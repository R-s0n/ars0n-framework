import React, {useState} from 'react';
import {ToastProvider} from 'react-toast-notifications';
import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Creative = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <>
        <div className="bg-secondary checklistStyle pt-4 ml-4">
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
        <div className="bg-secondary workTableStyle">
            {
                currentStep === 0 ?
                <ToastProvider><HopHeaders thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 1 ?
                <ToastProvider><CachePoisoning thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 8 ?
                <ToastProvider><CspBypass thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 9 ?
                <ToastProvider><Cors thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
        </div>
        </>
    )
}

export default Creative;