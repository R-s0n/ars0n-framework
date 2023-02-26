import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {useToasts} from 'react-toast-notifications';
import SubDomainResults from '../HelperComponents/SubDomainResults';
import SubDomainForm from '../HelperComponents/SubDomainForm';

const Ctl = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.ctl;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.ctl)
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

    const addCtlData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.ctl = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.ctl)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteCtlData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.ctl = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.ctl)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>Gets all subdomains to a domain by querying the database of the crt.sh Certificate Transparency search engine.</p>
                    <p><b>GOAL: </b>Identify valid sub-domains of the current FQDN to help build a complete picture of the application.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={copyToClipboard}>git clone https://github.com/hannob/tlshelpers.git</span></p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>sudo ./getsubdomain {props.thisFqdn.fqdn} | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="ctl" formFunction={addCtlData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteCtlData} subdomainList={subdomainList} thisScanner="ctl"/>
                }
            </div>
        </div>
    )
}

export default Ctl;