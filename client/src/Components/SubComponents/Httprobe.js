import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const Httprobe = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

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
    
    const copyToClipboard = e => {
        navigator.clipboard.writeText(e.target.innerText)
        addToast(`Copied "${e.target.innerText}" to Clipboard`, {appearance:'info',autoDismiss:true});
    }

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
                    <p><b>DETAILS: </b>Take a list of domains and probe for working http and https servers.</p>
                    <p><b>GOAL: </b>Iterate through the list of unique FQDNs to identify all domain names that are being hosted on live servers.</p>
                    <p><b>DOWNLOAD / Install: </b><span onClick={copyToClipboard}>go get -u github.com/tomnomnom/httprobe</span></p>
                    <p><b>RUN (Shallow): </b><span onClick={copyToClipboard}>cat consolidated.{props.thisFqdn.fqdn}.txt | httprobe &gt; httprobe.{props.thisFqdn.fqdn}.txt; cat httprobe.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                    <p><b>RUN (Deep): </b><span onClick={copyToClipboard}>cat consolidated.{props.thisFqdn.fqdn}.txt | httprobe &gt; httprobe.{props.thisFqdn.fqdn}.txt; cat httprobe.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
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