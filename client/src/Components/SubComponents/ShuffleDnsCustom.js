import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const ShuffleDnsCustom = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.shufflednsCustom;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.shufflednsCustom)
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

    const addShuffleDnsCustomData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.shufflednsCustom = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.shufflednsCustom)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteShuffleDnsCustomData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.shufflednsCustom = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.shufflednsCustom)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>ShuffleDNS is a wrapper around massdns written in go that allows you to enumerate valid subdomains using active bruteforce as well as resolve subdomains with wildcard handling and easy input-output support.</p>
                    <p><b>GOAL: </b>Bruteforce subdomains based on given wordlist.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={copyToClipboard}>GO111MODULE=on go get -v github.com/projectdiscovery/shuffledns/cmd/shuffledns</span></p>
                    <p><b>Run: </b><span onClick={copyToClipboard}>~/go/bin/shuffledns -d {props.thisFqdn.fqdn} -w ~/Wordlists/custom.txt -r ~/Wordlists/resolvers.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="shufflednsCustom" formFunction={addShuffleDnsCustomData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteShuffleDnsCustomData} subdomainList={subdomainList} thisScanner="shufflednsCustom"/>
                }
            </div>
        </div>
    )
}

export default ShuffleDnsCustom;