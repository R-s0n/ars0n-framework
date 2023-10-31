import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../Component.css';



const Logging = props => {
    const [currentStep, setCurrentStep] = useState(0);
    const [logs, setLogs] = useState([]);
    const [loaded, setLoaded] = useState(false);

    useEffect(()=>{
        axios.post('http://localhost:8000/api/log/all')
        .then((res) => {
            setLogs(res.data);
            setLoaded(true);
        })
    }, [])

    return (
        <div className="container-fluid">
            <div className="row">
                <div className="bg-secondary checklistStyle pt-2 col-3 ml-4">
                    <ul style={{"listStyleType":"none"}}>
                        <li></li>
                    {
                        logs.map((log, i) => {
                            return (
                                <li onClick={(e)=>setCurrentStep(i)}>{log['scan']}</li>
                            )
                        })
                    }
                    </ul>
                </div>
                <div className="bg-secondary workTableStyle col-8 pt-3 pl-3">
                    {
                        logs.length > 0 && logs[currentStep]['logFile'].map((log, i) => {
                            return (
                                <span style={{display: "block"}}>{log}</span>
                            )
                        })
                    }
                </div>
            </div>
        </div>
    )
}

export default Logging;