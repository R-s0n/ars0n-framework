import React, {useState} from 'react';

import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Creative = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 ml-4 col-3">
            <ul>
                <li>Internal</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Indirect Object Reference (IDOR)</li>
                    <li onClick={(e)=>setCurrentStep(1)}>HTTP Parameter Pollution</li>
                </ul>
                <li>External</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(2)}>Subdomain Takeover</li>
                    <li onClick={(e)=>setCurrentStep(3)}>GitHub Sensitive Data Leak</li>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
            {
                currentStep === 0 ?
                <HopHeaders thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 1 ?
                <CachePoisoning thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 8 ?
                <CspBypass thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 9 ?
                <Cors thisFqdn={props.thisFqdn} /> :
                ''
            }
        </div>
        </div>
        </div>
    )
}

export default Creative;