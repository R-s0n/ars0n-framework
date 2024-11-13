import toast, { Toaster } from 'react-hot-toast';
import UrlForm from '../HelperComponents/UrlForm';

const Subjack = props => {


    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }



    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>Subjack is a Subdomain Takeover tool written in Go designed to scan a list of subdomains concurrently and identify ones that are able to be hijacked. With Go's speed and efficiency, this tool really stands out when it comes to mass-testing. Always double check the results manually to rule out false positives.</p>
                    <p><b>GOAL: </b>Identify potential targets for a Hostile Subdomain Takeover attack.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={notify}>go get github.com/haccer/subjack</span></p>
                    <p><b>RUN: </b><span onClick={notify}>./subjack -w consolidated.{props.thisFqdn.fqdn}.txt -t 100 -timeout 45 -o subjack.{props.thisFqdn.fqdn}.txt -ssl</span></p>
                </div>
            </div>
            <div className="row">
                <UrlForm thisFqdn={props.thisFqdn} thisScanner="subjack"/>
            </div>
        </div>
    )
}

export default Subjack;