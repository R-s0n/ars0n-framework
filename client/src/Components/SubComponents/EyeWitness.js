import React from 'react';

import toast, { Toaster } from 'react-hot-toast';
import UrlForm from '../HelperComponents/UrlForm';

const EyeWitness = props => {


    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }



    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>EyeWitness is designed to take screenshots of websites provide some server header info, and identify default credentials if known.</p>
                    <p><b>GOAL: </b>Using the list of FQDNs and Subdomains found to be running on active servers (Httprobe), use EyeWitness to identy potentially vulnerable targets.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={notify}>git clone https://github.com/FortyNorthSecurity/EyeWitness.git; cd EyeWitness/Python/setup; sudo ./setup.sh; cd ../../;</span></p>
                    <p><b>RUN: </b><span onClick={notify}>./EyeWitness.py -f httproxy.{props.thisFqdn.fqdn}.txt</span></p>
                </div>
            </div>
            <div className="row">
                <UrlForm thisFqdn={props.thisFqdn} thisScanner="eyeWitness"/>
            </div>
        </div>
    )
}

export default EyeWitness;