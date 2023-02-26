import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const Dnmasscan = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.masscan;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.masscan)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])
    
    const copyToClipboard = e => {
        navigator.clipboard.writeText(e.target.innerText)
        addToast(`Copied "${e.target.innerText}" to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    const addDnmasscanData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.masscan = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.masscan)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteDnmasscanData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.masscan = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.masscan)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-3">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>Dnmasscan is a bash script to automate resolving a file of domain names and subsequentlly scanning them using masscan.  As masscan does not accept domain names, a file is created (specified in the second argument to the script) which will log which IP addresses resolve to which domain names for cross reference after the script has finished executing.</p>
                    <p><b>GOAL: </b>Using the consolidated list of subdomains, this tool will identify a large number of the servers our target is running and perform a full port scan on them.</p>
                    <p><b>DOWNLOAD: </b><span onClick={copyToClipboard}>https://github.com/rastating/dnmasscan.git</span></p>
                    <p><b>INSTALL: </b><span onClick={copyToClipboard}>sudo apt-get --assume-yes install git make gcc; git clone https://github.com/robertdavidgraham/masscan; cd masscan; make; make install;</span></p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>sudo ./dnmasscan /tmp/dnmasscan.tmp /tmp/dns.log -p1-65535 --rate=500 | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="masscan" formFunction={addDnmasscanData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteDnmasscanData} subdomainList={subdomainList} thisScanner="masscan"/>
                }
            </div>
        </div>
    )
}

export default Dnmasscan;