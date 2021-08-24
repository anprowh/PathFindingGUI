import { useEffect, useState, } from 'react'


const colors = new Map([
    ['S', '#00FF00'],
    ['E', '#0000FF'],
    ['*', '#FF0000'],
    ['o', '#FF00FF']
])

const getCellColor = (weight, cell_type) => {
    if (colors.has(cell_type))
        return colors.get(cell_type)
    const brightness = Math.floor(255 - ((-(Math.pow(1.1, (-(weight / 2)))) + 1) * 255)).toString()
    return 'rgb(' + brightness + ',' + brightness + ',' + brightness + ')'
}

const getTextColor = (weight, cell_type) => {
    if (colors.has(cell_type))
        return "#000000"
    const brightness = Math.floor(255 - ((-(Math.pow(1.1, (-(weight / 2)))) + 1) * 255))
    return (brightness > 127 ? "#000000" : "#FFFFFF")
}


const Grid = ({mouseDown=false,setMouseDown=()=>{}}) => {

    const [grid, setGrid] = useState([])
    const [types, setTypes] = useState([])

    const [sessionId, setSessionId] = useState(1)
    const [currentStep, setCurrentStep] = useState(0)
    const [working, setWorking] = useState(false)
    const [updated, setUpdated] = useState(false)
    const [apiMayNotWork, setApiMayNotWork] = useState(false)
    const [nSteps, setNSteps] = useState(0)
    const [fillValue, setFillValue] = useState(0)
    const [envId, setEnvId] = useState(0)
    const [speed, setSpeed] = useState(100)

    const fetchSession = async () => {
        const res = await fetch('http://192.168.1.57:8000/session', {credentials: 'include'})
        const data = await res.json()

        return data
    }
    
    const fetchGrid = async () => {
        const res = await fetch('http://192.168.1.57:8000/env?session_id='+sessionId, {credentials: 'include'})
        const data = await res.json()

        return data
    }

    const fetchNewGrid = async () => {
        const res = await fetch('http://192.168.1.57:8000/env/'+envId+'?session_id='+sessionId, {credentials: 'include'})
        const data = await res.json()

        return data
    }

    const fetchTypes = async () => {
        const res = await fetch('http://192.168.1.57:8000/step/' + currentStep+'?session_id='+sessionId, {credentials: 'include'})
        const data = await res.json()

        return data
    }

    const postNewWeight = async (x,y,weight) => {
        await fetch('http://192.168.1.57:8000/set_weight?session_id='+sessionId, 
             {method: 'POST',
              headers: {
                'Content-Type': 'application/json;charset=utf-8'
              },
              body: JSON.stringify({x: x, y: y, weight: weight})
             })
    }

    const saveEnvironment = async () => {
        await fetch('http://192.168.1.57:8000/save_env/'+fillValue+'?session_id='+sessionId, {method: 'POST'})
        setEnvId(fillValue)
    }


    useEffect(() => {
        const getSessionId = async () => {
            const retrievedSessionId = await fetchSession()
            setSessionId(retrievedSessionId.session_id)
        }

        getSessionId()
    }, [])

    useEffect(() => {
        const getGrid = async () => {
            const retrievedGrid = await fetchGrid()
            const retrievedTypes = await fetchTypes()
            setGrid(retrievedGrid.environment)
            setTypes(retrievedTypes)
            setNSteps(retrievedGrid.n_steps)
            setUpdated(false)
        }

        getGrid()
        setApiMayNotWork(false)
    }, [updated])

    useEffect(() => {
        const getGrid = async () => {
            const retrievedGrid = await fetchNewGrid()
            const retrievedTypes = await fetchTypes()
            setGrid(retrievedGrid.environment)
            setTypes(retrievedTypes)
            setNSteps(retrievedGrid.n_steps)
        }

        getGrid()
        setApiMayNotWork(false)
    }, [envId, sessionId])

    useEffect(() => {
        const getTypes = async () => {
            const retrievedTypes = await fetchTypes()
            setTypes(retrievedTypes)
        }

        getTypes()
        setApiMayNotWork(false)
    }, [currentStep, envId, sessionId])

    useEffect(() => {
        const timeout = setTimeout(() => {
            if (working){
                setCurrentStep(currentStep + 1)
                if (currentStep >= nSteps - 1)
                    setWorking(false)
            }
        }, speed)
        return () => { clearTimeout(timeout) }
    }, [currentStep, working, envId, speed, sessionId])

    useEffect(() => {
        const timeout = setTimeout(() => {
            try {
                if (grid.length===0)
                    setApiMayNotWork(true)
            }
            catch {
                setApiMayNotWork(true)
            }
        }, 2000)
    }, [envId, sessionId, updated])

    
    useEffect(() => {
        const callback = (event) => {
            if (event.key === ' ') {
                if (currentStep >= nSteps - 1)
                    setCurrentStep(0)
                setWorking(!working)
            }
            else if (!isNaN(event.key)) {
                setFillValue(+(fillValue+event.key))
            }
            else if (event.key === 'Backspace') {
                setFillValue(Math.floor(fillValue/10))
            }
            else if (event.key === 'l') {
                setCurrentStep(0)
                setEnvId(fillValue)
                setWorking(false)
            }
            else if (event.key === 'r') {
                setCurrentStep(0)
                setWorking(false)
            }
            else if (event.key === 's') {
                saveEnvironment()
                alert('Environment saved to id: ' + fillValue)
            }
            else if (event.key === 'ArrowRight') {
                setSpeed(speed/2)
            }
            else if (event.key === 'ArrowLeft') {
                setSpeed(speed*2)
            }
            else {
                console.log(event.key)
            }
        }

        window.addEventListener('keydown', callback)

        return ()=>window.removeEventListener('keydown', callback)
    })

    const changeWeightOver = (x, y, currentWeight) => {
        if (currentWeight !== fillValue && mouseDown){
            postNewWeight(x, y, fillValue)
            setUpdated(true)
        }
    }

    const onMouseDown = (x, y, currentWeight) => {
        setMouseDown(true)
        if (currentWeight !== fillValue){
            postNewWeight(x, y, fillValue)
            setUpdated(true)
        }
    }
    const onMouseUp = (e) => {setMouseDown(false)}

    try{
        if (grid.length===types.length && grid[0].length===types[0].length)
        return (
            <>
                <p style={{marginLeft: '10px'}}>{sessionId}</p>
                <table className='grid'>
                    <tbody>
                        {
                            grid.map((row, i) => (
                                <tr key={i}>{row.map((element, j) => (
                                    <td key={i * row.length + j}
                                        style={{
                                            backgroundColor: getCellColor(element, types[i][j]), color: getTextColor(element, types[i][j]),
                                            width: 'calc(60vmin/' + Math.max(row.length, grid.length) + ')',
                                            minHeight: 'calc(60vmin/' + Math.max(row.length, grid.length) + ')',
                                            lineHeight: 'calc(60vmin/' + Math.max(row.length, grid.length) + ')',
                                            userSelect: 'none',
                                        }} 
                                        onMouseOver={(e)=>changeWeightOver(i,j,element)} 
                                        onMouseDown={(e)=>onMouseDown(i,j,element)}
                                        onMouseUp={onMouseUp}>
                                        {element}
                                    </td>)
                                )}</tr>
                            ))
                        }
                    </tbody>
                </table>
                <p style={{marginLeft: '10px'}}>{fillValue}</p>
            </>)
    } catch {}
    return <div style={{marginLeft: '10px'}}>
                <p>Loading...</p>
                <p>{apiMayNotWork?"API may not be working or session is invalid. Try to reload":""}</p>
           </div>
    
}

export default Grid
