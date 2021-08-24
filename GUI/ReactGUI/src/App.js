import './App.css';
import Header from './components/Header'
import Grid from './components/Grid'
import { useState } from 'react'

document.title = 'Pathfinding Algorithm Demo'



function App() {
  
    const [mouseDown, setMouseDown] = useState(false)

  
    const onMouseDown = (e) => {setMouseDown(true)}

    const onMouseUp = (e) => {setMouseDown(false)}

    return (
        <div className="App" onMouseDown={onMouseDown} onMouseUp={onMouseUp}>
        <Header />
        <Grid mouseDown={mouseDown} setMouseDown={setMouseDown} />
        </div>
    );
}

export default App;
