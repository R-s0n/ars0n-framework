import React, {useState} from 'react';

import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Bypass = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <>
        <div className="bg-secondary checklistStyle pt-4 ml-4">
            <ul>
                <li>Authentication Bypass</li>
                <ul>
                    <li>Cookie Testing</li>
                    <ul style={{listStyleType: "none"}}>
                        <li onClick={(e)=>setCurrentStep(11)}>Basic Checks</li>
                        <li onClick={(e)=>setCurrentStep(12)}>Decode/Modify Cookie Values</li>
                        <li onClick={(e)=>setCurrentStep(13)}>Session Fixation</li>
                        <li onClick={(e)=>setCurrentStep(14)}>Cookie Tossing</li>
                        <li onClick={(e)=>setCurrentStep(15)}>Padding Oracle Attack</li>
                    </ul>
                    <li onClick={(e)=>setCurrentStep(0)}>2FA/OTP Bypass</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Payment Process Bypass</li>
                    <li onClick={(e)=>setCurrentStep(2)}>Captcha Bypass</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Race Conditions</li>
                    <li onClick={(e)=>setCurrentStep(4)}>Rate Limit Bypass</li>
                    <li onClick={(e)=>setCurrentStep(5)}>Reset Forgotten Password Bypass</li>
                    <li onClick={(e)=>setCurrentStep(6)}>Registration Vulnerabilities</li>
                </ul>
                <li>Access Control Bypass</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(8)}>Insecure Management Interface</li>
                    <li onClick={(e)=>setCurrentStep(9)}>Insecure Source-Code Management</li>
                </ul>
                <li>Account Takeover</li>
                <ul>
                    <li>OAuth Account Takeover</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(10)}>Grant Type -- Authorization Code</li>
                        <li onClick={(e)=>setCurrentStep(11)}>Grant Type -- Implicit</li>
                        <li onClick={(e)=>setCurrentStep(12)}>OpenID Connect w/ OAuth</li>
                    </ul>
                    <li onClick={(e)=>setCurrentStep(13)}>SAML Attacks</li>
                    <li onClick={(e)=>setCurrentStep(14)}>Padding Oracle Attack</li>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle">
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
        </>
    )
}

export default Bypass;