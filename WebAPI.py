import sys
import uvicorn
from logging import Logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Algorithms.SimplePF import SimplePF
from Algorithms.TwoSidesPF import TwoSidesPF
from Algorithms.AStar import AStar
from SearchEnvironment import SearchEnvironment


class SessionIdManager:
    def __init__(self):
        self.current_id = 2
        self._used_ids = []

    def get_new_id(self):
        self.current_id += 1
        self._used_ids.append(self.current_id)
        return self.current_id

    def get_last_id(self):
        return self._used_ids[-1]

    def remove_id(self, id_to_remove: int):
        self._used_ids.remove(id_to_remove)


class EnvChange(BaseModel):
    x: int
    y: int
    weight: int


app = FastAPI()

# Managing CORS

origins = [
    'http://192.168.1.57:3000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining environment which appears as the starting environment for every session
standard_environment = SearchEnvironment(21, 20, 3, 16, 15, 5)

arg_to_alg_dict = {'simple': SimplePF, 'two_sides': TwoSidesPF, 'a_star': AStar}
try:
    algorithm = arg_to_alg_dict[sys.argv[1]](standard_environment)
except KeyError:
    algorithm = SimplePF(standard_environment)

# For every session steps are precomputed every time env changes
to_display_dict = {}
session_id_env_dict = {}


def precompute_steps(environment: SearchEnvironment):
    algorithm.environment = environment
    algorithm.reset()
    to_display = []
    while not algorithm.done:
        to_display.append(algorithm.get_types_grid())
        algorithm.next_step()
    to_display.append(algorithm.get_types_grid())
    return to_display


id_manager = SessionIdManager()
logger = Logger('WebAPI')


def create_session_non_async():
    new_id = id_manager.get_new_id()
    session_id_env_dict[new_id] = standard_environment
    to_display_dict[new_id] = precompute_steps(session_id_env_dict[new_id])
    return new_id


@app.get('/session')
async def set_session():
    return {'session_id': create_session_non_async()}


@app.get('/env')
async def env(session_id: int):
    if session_id not in session_id_env_dict.keys():
        return {'environment': [[]], 'n_steps': 1}
    return {'environment': session_id_env_dict[int(session_id)].get_grid(), 'n_steps': len(to_display_dict[session_id])}


@app.get('/env/{env_id}')
async def env(env_id: int, session_id: int):
    if session_id not in session_id_env_dict.keys():
        return {'environment': [[]], 'n_steps': 1}
    session_id_env_dict[int(session_id)] = SearchEnvironment.load(env_id)
    to_display_dict[session_id] = precompute_steps(session_id_env_dict[int(session_id)])
    return {'environment': session_id_env_dict[session_id].get_grid(), 'n_steps': len(to_display_dict[session_id])}


@app.get('/step/{n_step}')
async def step(n_step: int, session_id: int):
    if session_id not in session_id_env_dict.keys():
        return [[]]
    return to_display_dict[session_id][min(n_step, len(to_display_dict[session_id]) - 1)]


@app.post('/set_weight')
async def set_weight(change: EnvChange, session_id: int):
    if session_id not in session_id_env_dict.keys():
        return {'environment': [[]], 'n_steps': 1}
    session_id_env_dict[session_id].set_weight(change.x, change.y, change.weight)
    to_display_dict[session_id] = precompute_steps(session_id_env_dict[int(session_id)])
    return {'environment': session_id_env_dict[session_id].get_grid(), 'n_steps': len(to_display_dict[session_id])}


@app.post('/save_env/{file_id}')
async def save_env(file_id: int, session_id: int):
    if session_id not in session_id_env_dict.keys():
        return {}
    session_id_env_dict[session_id].save(file_id)
    return {}


if __name__ == '__main__':
    uvicorn.run('WebAPI:app', host='0.0.0.0', reload=True, port=8000)
