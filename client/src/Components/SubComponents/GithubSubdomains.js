import axios from 'axios';
import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import SubDomainForm from '../HelperComponents/SubDomainForm';
import SubDomainResults from '../HelperComponents/SubDomainResults';


const GithubSubdomains = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([])
    const [loaded, setLoaded] = useState(false);

    const {addToast} = useToasts()

    useEffect(()=>{
        setFormCompleted(false);
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.githubSearch;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.githubSearch)
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

    const addGithubSubdomainsData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.githubSearch = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.githubSearch)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteGithubSubdomainsData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.githubSearch = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.githubSearch)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                <p><b>DETAILS: </b>Find additional subdomains on GitHub. Very useful during you recon phase, you will probably get some extras subdomains other tools didn’t find because not public.</p>
                    <p><b>GOAL: </b>Scape public GitHub repos for additional subdomains.</p>
                    <p><b>DOWNLOAD: </b><span onClick={copyToClipboard}>git clone https://github.com/gwen001/github-search.git</span></p>
                    <p><b>INSTALL: </b><span onClick={copyToClipboard}>pip3 install -r requirements2.txt</span></p>
                    <p><b>RUN: </b><span onClick={copyToClipboard}>python3 github-subdomains.py -d {props.thisFqdn.fqdn} -t $github_apikey &et; githubsubdomains.{props.thisFqdn.fqdn}.txt; cat githubsubdomains.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
                {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="githubSearch" formFunction={addGithubSubdomainsData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteGithubSubdomainsData} subdomainList={subdomainList} thisScanner="githubSearch"/>
                }
            </div>
        </div>
    )
}

export default GithubSubdomains;