import React, {useState} from 'react';
import {ToastProvider} from 'react-toast-notifications';
import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Feature = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <>
        <div className="bg-secondary checklistStyle pt-4 ml-4">
            <ul>
                <li>Structured Objects</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Deserialization</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(1)}>Java</li>
                        <li onClick={(e)=>setCurrentStep(2)}>.NET</li>
                        <li onClick={(e)=>setCurrentStep(3)}>PHP</li>
                        <li onClick={(e)=>setCurrentStep(4)}>Python</li>
                        <li onClick={(e)=>setCurrentStep(5)}>NodeJS</li>
                        <li onClick={(e)=>setCurrentStep(6)}>Ruby</li>
                    </ul>
                    <li onClick={(e)=>setCurrentStep(7)}>Json Web Tokens (JWT)</li>
                    <li onClick={(e)=>setCurrentStep(8)}>XML External Entity (XXE) Injection</li>
                </ul>
                <li>Files</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(9)}>File Upload</li>
                    <li onClick={(e)=>setCurrentStep(10)}>Formula Injection</li>
                    <li onClick={(e)=>setCurrentStep(11)}>PDF Injection</li>
                    <li onClick={(e)=>setCurrentStep(12)}>Server-Side XSS</li>
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

export default Feature;