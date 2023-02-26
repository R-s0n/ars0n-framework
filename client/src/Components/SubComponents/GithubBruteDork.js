import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import axios from 'axios';
import GithubSearchForm from '../HelperComponents/GithubSearchForm';
import GithubSearchResults from '../HelperComponents/GithubSearchResults';

const GithubSearch = props => {
    const {addToast} = useToasts()
    const [formCompleted, setFormCompleted] = useState(false);

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                const tempArr = res.data.recon.osint.GithubSearch;
                if (tempArr.length > 0){
                    setFormCompleted(true);
                }
            })
    }, [props.thisFqdn._id])

    const copyToClipboard = e => {
        navigator.clipboard.writeText(e.target.innerText)
        addToast(`Copied "${e.target.innerText}" to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    const thisFormCompleted = (completed) => {
        setFormCompleted(completed);
    }

    return (
        <div className="container mt-4">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>This tool is a quick and easy Python script designed to identify Github search terms that can yield potentially valuable results for security researchers and bug bounty hunters. Using the Github api, this script will perform search repos associated with a target organization and return a list of the searches sorted by the number of results. This will allow researchers to identify potential code stored in Github that may contain sensitive information.</p>
                    <p><b>GOAL: </b>Identify Github dorks with potentially valuable results, helping to prioritize manual searches</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={copyToClipboard}>git clone https://github.com/R-s0n/Github_Brute-Dork.git</span></p>
                    <p><b>RUN (Shallow - 170 Results): </b><span onClick={copyToClipboard}>python github_brutedork.py -o {props.thisFqdn.fqdn} -u [GITHUB USERNAME] -t [GITHUB PERSONAL ACCESS TOKEN]</span></p>
                    <p><b>RUN (Deep - 1760 Results): </b><span onClick={copyToClipboard}>python github_brutedork.py -o {props.thisFqdn.fqdn} -u [GITHUB USERNAME] -t [GITHUB PERSONAL ACCESS TOKEN] -d</span></p>
                </div>
            </div>
            <div className="row">
                {
                    formCompleted === false ?
                    <GithubSearchForm thisFqdn={props.thisFqdn} thisFormCompleted={thisFormCompleted} /> :
                    <GithubSearchResults thisFqdn={props.thisFqdn} thisFormCompleted={thisFormCompleted} />
                }
            </div>
        </div>
    )
}

export default GithubSearch;