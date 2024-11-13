import { useState, useEffect } from 'react';
import axios from 'axios';
import toast, { Toaster } from 'react-hot-toast';
import SubDomainResults from '../HelperComponents/SubDomainResults';
import SubDomainForm from '../HelperComponents/SubDomainForm';

const Gau = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);



    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }

    useEffect(()=>{
        axios.post(`http://${process.env.REACT_APP_API_IP}:${process.env.REACT_APP_API_PORT}/api/fqdn`, {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.gau;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.gau)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props.thisFqdn._id])
    


    const addGauData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.gau = list.split("\n");
        axios.post(`http://${process.env.REACT_APP_API_IP}:${process.env.REACT_APP_API_PORT}/api/fqdn/update`, tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.gau)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteGauData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.gau = [];
        axios.post(`http://${process.env.REACT_APP_API_IP}:${process.env.REACT_APP_API_PORT}/api/fqdn/update`, tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.gau)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>Getallurls (gau) fetches known URLs from AlienVault's Open Threat Exchange, the Wayback Machine, and Common Crawl for any given domain. Inspired by Tomnomnom's waybackurls.</p>
                    <p><b>GOAL: </b>Identify valid sub-domains of the current FQDN to help build a complete picture of the application.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={notify}>GO111MODULE=on go get -u -v github.com/lc/gau</span></p>
                    <p><b>RUN: </b><span onClick={notify}>sudo gau -subs {props.thisFqdn.fqdn} | cut -d / -f 3 | sort -u &gt; gau.{props.thisFqdn.fqdn}.txt; cat gau.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
            {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="gau" formFunction={addGauData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteGauData} subdomainList={subdomainList} thisScanner="gau"/>
                }
            </div>
        </div>
    )
}

export default Gau;