import axios from 'axios';import React, {useState, useEffect} from 'react';

import toast, { Toaster } from 'react-hot-toast';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const Httprobe = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);



    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.httprobe;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.httprobe)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])
    


    const addHttprobeData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.httprobe = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.httprobe)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteHttprobeData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.httprobe = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.httprobe)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>Take a list of domains and probe for working http and https servers.</p>
                    <p><b>GOAL: </b>Iterate through the list of unique FQDNs to identify all domain names that are being hosted on live servers.</p>
                    <p><b>DOWNLOAD / Install: </b><span onClick={notify}>go get -u github.com/tomnomnom/httprobe</span></p>
                    <p><b>RUN (Shallow): </b><span onClick={notify}>cat consolidated.{props.thisFqdn.fqdn}.txt | httprobe &gt; httprobe.{props.thisFqdn.fqdn}.txt; cat httprobe.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                    <p><b>RUN (Deep): </b><span onClick={notify}>cat consolidated.{props.thisFqdn.fqdn}.txt | httprobe &gt; httprobe.{props.thisFqdn.fqdn}.txt; cat httprobe.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
            {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="httprobe" formFunction={addHttprobeData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteHttprobeData} subdomainList={subdomainList} thisScanner="httprobe"/>
                }
            </div>
        </div>
    )
}

export default Httprobe;