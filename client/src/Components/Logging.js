import React, {useState} from 'react';
import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import LogEntry from './SubComponents/LogEntry';



const Bypass = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 col-3 ml-4">
            <ul style={{"listStyleType":"none"}}>
                <li onClick={(e)=>setCurrentStep(0)}>Wildfire.py -- 12 Oct 2023 12:36pm</li>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
            {
                currentStep === 0 ?
                <LogEntry thisFqdn={props.thisFqdn} /> :
                ''
            }
        </div>
        </div>
        </div>
    )
}

export default Bypass;