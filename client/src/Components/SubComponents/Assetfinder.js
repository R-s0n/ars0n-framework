import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {useToasts} from 'react-toast-notifications';
import SubDomainResults from '../HelperComponents/SubDomainResults';
import SubDomainForm from '../HelperComponents/SubDomainForm';

const Assetfinder = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.assetfinder;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.assetfinder)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props.thisFqdn._id])
    
    const copyToClipboard = e => {
        navigator.clipboard.writeText(e.target.innerText)
        addToast(`Copied "${e.target.innerText}" to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    const addAssetfinderData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.assetfinder = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.assetfinder)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteAssetfinderData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.assetfinder = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.assetfinder)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>Find domains and subdomains potentially related to a given domain. (straight to the point as usual, Tomnomnom!)</p>
                    <p><b>GOAL: </b>Identify valid sub-domains of the current FQDN to help build a complete picture of the application.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={copyToClipboard}>go get -u github.com/tomnomnom/assetfinder</span></p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>sudo assetfinder --subs-only {props.thisFqdn.fqdn} &gt; assetfinder.{props.thisFqdn.fqdn}.txt; cat assetfinder.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
            {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="assetfinder" formFunction={addAssetfinderData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteAssetfinderData} subdomainList={subdomainList} thisScanner="assetfinder"/>
                }
            </div>
        </div>
    )
}

export default Assetfinder;