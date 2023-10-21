import React, {useState} from 'react';
import '../Component.css';
import ResourceEntry from './SubComponents/ResourceEntry';
import Portswigger from './SubComponents/Portswigger';




const Feature = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 ml-4 col-3">
            <ul  style={{"listStyleType":"none"}}>
                <li style={{"fontWeight":"bold"}}>Red Team AppSec Resources</li>
                <ul  style={{"listStyleType":"none"}}>
                    <li onClick={(e)=>setCurrentStep(0)}>Portswigger</li>
                    <li onClick={(e)=>setCurrentStep(1)}>HackTricks</li>
                    <li onClick={(e)=>setCurrentStep(1)}>PenTesterLab</li>
                    <li onClick={(e)=>setCurrentStep(1)}>HackTheBox</li>
                    <li onClick={(e)=>setCurrentStep(1)}>PayloadsAllTheThings</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Bug Bounty Programs</li>
                </ul>
                <li style={{"fontWeight":"bold"}}>Blue Team AppSec Resources</li>
                <ul  style={{"listStyleType":"none"}}>
                    <li onClick={(e)=>setCurrentStep(1)}>OWASP Cheat Sheet</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Codecademy</li>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
        {
                currentStep === 0 ?
                <Portswigger thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 1 ?
                <ResourceEntry thisFqdn={props.thisFqdn} /> :
                ''
            }
        </div>
        </div>
        </div>
    )
}

export default Feature;