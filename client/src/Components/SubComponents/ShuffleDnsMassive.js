import axios from 'axios';import React, {useState, useEffect} from 'react';

import toast, { Toaster } from 'react-hot-toast';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const ShuffleDnsMassive = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);



    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }

    useEffect(()=>{
        setFormCompleted(false);
        axios.post(`http://${process.env.API_IP}:${process.env.API_PORT}/api/fqdn`, {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.shuffledns;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.shuffledns)
                        setFormCompleted(true);
                    }
                }
                setLoaded(true);
            })
    }, [props])
    


    const addShuffleDnsMassiveData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.shuffledns = list.split("\n");
        axios.post(`http://${process.env.API_IP}:${process.env.API_PORT}/api/fqdn/update`, tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.shuffledns)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteShuffleDnsMassiveData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.shuffledns = [];
        axios.post(`http://${process.env.API_IP}:${process.env.API_PORT}/api/fqdn/update`, tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.shuffledns)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>ShuffleDNS is a wrapper around massdns written in go that allows you to enumerate valid subdomains using active bruteforce as well as resolve subdomains with wildcard handling and easy input-output support.</p>
                    <p><b>GOAL: </b>Bruteforce subdomains based on given wordlist.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={notify}>GO111MODULE=on go get -v github.com/projectdiscovery/shuffledns/cmd/shuffledns</span></p>
                    <p><b>Run: </b><span onClick={notify}>~/go/bin/shuffledns -d {props.thisFqdn.fqdn} -w ~/Wordlists/all.txt -r ~/Wordlists/resolvers.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="shuffledns" formFunction={addShuffleDnsMassiveData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteShuffleDnsMassiveData} subdomainList={subdomainList} thisScanner="shuffledns"/>
                }
            </div>
        </div>
    )
}

export default ShuffleDnsMassive;