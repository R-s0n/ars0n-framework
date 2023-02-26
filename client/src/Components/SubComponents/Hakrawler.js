import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const Hakrawler = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.hakrawler;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.hakrawler)
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

    const addHakrawlerData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.hakrawler = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.hakrawler)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteHakrawlerData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.hakrawler = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.hakrawler)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>Hakrawler is a Go web crawler designed for easy, quick discovery of endpoints and assets within a web application. It can be used to discover:</p>
                    <p><b>GOAL: </b>The goal is to create the tool in a way that it can be easily chained with other tools such as subdomain enumeration tools and vulnerability scanners in order to facilitate tool chaining, for example: assetfinder target.com | hakrawler | some-xss-scanner</p>
                    <p><b>DOWNLOAD: </b><span onClick={copyToClipboard}>go get github.com/hakluke/hakrawler</span></p>
                    <p><b>INSTALL: </b><span onClick={copyToClipboard}>apt-get install golang</span></p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>cat /tmp/amass.tmp | ./hakrawler -subs -d 3 -u &gt; hakrawler.{props.thisFqdn.fqdn}.txt; cat hakrawler.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p> 
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="hakrawler" formFunction={addHakrawlerData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteHakrawlerData} subdomainList={subdomainList} thisScanner="hakrawler"/>
                }
            </div>
        </div>
    )
}

export default Hakrawler;