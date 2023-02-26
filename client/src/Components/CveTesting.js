import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {ToastProvider} from 'react-toast-notifications';
import '../Component.css';
import NucleiScans from './SubComponents/NucleiScans';


const CveTesting = props => {
    const [currentStep, setCurrentStep] = useState(0);
    const [impactfulVulnCount, setImpactfulVulnCount] = useState(0)

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    let counter = 0;
                    for (let i=0; i<res.data.vulns.length; i++){
                        if (res.data.vulns[i].info.severity !== "info"){
                            counter++;
                        }
                    }
                    setImpactfulVulnCount(counter);
                }
            })
    }, [props])

    return (
        <>
        <div className="bg-secondary checklistStyle pt-4 ml-4">
            <ul>
                <li>Third-Party Scanning</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Nuclei Scan Results (Impactful: {impactfulVulnCount})</li>
                </ul>
                <li>Custom Scanning</li>
                <ul>
                    <li>CVE Scanning</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(1)}>Add CVE</li>
                        <li onClick={(e)=>setCurrentStep(2)}>CVE Scan Results</li>
                    </ul>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle">
            {
                currentStep === 0 ?
                <ToastProvider><NucleiScans thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
        </div>
        </>
    )
}

export default CveTesting;