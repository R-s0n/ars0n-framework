import React, {useState, useEffect} from 'react';
import axios from 'axios';
import {useToasts} from 'react-toast-notifications';
import SubDomainResults from '../HelperComponents/SubDomainResults';
import SubDomainForm from '../HelperComponents/SubDomainForm';

const Amass = props => {
    const [formCompleted, setFormCompleted] = useState(false);
    const [subdomainList, setSubdomainList] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const regex = "{1,3}"

    const {addToast} = useToasts()

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    const tempArr = res.data.recon.subdomains.amass;
                    if (tempArr.length > 0){
                        setSubdomainList(res.data.recon.subdomains.amass)
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

    const addAmassData = (list) => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.amass = list.split("\n");
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.amass)
                setFormCompleted(true);
            })
            .catch(err=>console.log(err));
    }

    const deleteAmassData = () => {
        const tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.amass = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                setSubdomainList(res.data.recon.subdomains.amass)
                setFormCompleted(false);
            })
    }

    return (
        <div className="container mt-4">
            <div className="row">
                <div className="col-12">
                    <p><b>DETAILS: </b>The OWASP Amass Project performs network mapping of attack surfaces and external asset discovery using open source information gathering and active reconnaissance techniques.  Amass is an incredibly powerful tool with a variety of features.  For a full list of functionality, click <a href="https://github.com/OWASP/Amass/blob/master/doc/tutorial.md" target="_blank" rel="noreferrer">here</a>.</p>
                    <p><b>GOAL: </b>Identify valid sub-domains of the current FQDN to help build a complete picture of the application.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={copyToClipboard}>apt-get install amass</span></p>
                    <p><b>RUN (PASSIVE): </b><span onClick={copyToClipboard}>amass enum --passive -d {props.thisFqdn.fqdn} -o {props.thisFqdn.fqdn}.txt; cat {props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                    <p><b>RUN (ACTIVE): </b><span onClick={copyToClipboard}>amass enum  -src -ip -brute -min-for-recursive 2 -d {props.thisFqdn.fqdn} -o amass.{props.thisFqdn.fqdn}.txt; cp amass.{props.thisFqdn.fqdn}.txt amass.{props.thisFqdn.fqdn}.full.txt; sed -i -E 's/\[(.*?)\] +//g' amass.{props.thisFqdn.fqdn}.txt; sed -i -E 's/ ([0-9]{regex}\.)[0-9].*//g' amass.{props.thisFqdn.fqdn}.txt; cat amass.{props.thisFqdn.fqdn}.txt | xclip -i -selection clipboard</span></p>
                </div>
            </div>
            <div className="row">
            {
                    loaded && formCompleted === false ?
                    <SubDomainForm thisFqdn={props.thisFqdn} thisScanner="amass" formFunction={addAmassData}/> :
                    <SubDomainResults thisFqdn={props.thisFqdn} resultsFunction={deleteAmassData} subdomainList={subdomainList} thisScanner="amass"/>                }
            </div>
        </div>
    )
}

export default Amass;