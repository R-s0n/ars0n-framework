import React from 'react';
import {useToasts} from 'react-toast-notifications';
import UrlForm from '../HelperComponents/UrlForm';

const EyeWitness = props => {
    const {addToast} = useToasts()

    const copyToClipboard = e => {
        navigator.clipboard.writeText(e.target.innerText)
        addToast(`Copied "${e.target.innerText}" to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>EyeWitness is designed to take screenshots of websites provide some server header info, and identify default credentials if known.</p>
                    <p><b>GOAL: </b>Using the list of FQDNs and Subdomains found to be running on active servers (Httprobe), use EyeWitness to identy potentially vulnerable targets.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={copyToClipboard}>git clone https://github.com/FortyNorthSecurity/EyeWitness.git; cd EyeWitness/Python/setup; sudo ./setup.sh; cd ../../;</span></p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>./EyeWitness.py -f httproxy.{props.thisFqdn.fqdn}.txt</span></p>
                </div>
            </div>
            <div className="row">
                <UrlForm thisFqdn={props.thisFqdn} thisScanner="eyeWitness"/>
            </div>
        </div>
    )
}

export default EyeWitness;