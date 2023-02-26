import React, {useState, useEffect} from 'react';
import {useToasts} from 'react-toast-notifications';
import axios from 'axios';

const Consolidator = props => {
    const [consolidatedList, setConsolidatedList] = useState([]);
    const [consolidatedNewList, setConsolidatedNewList] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const [refresh, setRefresh] = useState(0);

    const {addToast} = useToasts()

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                setConsolidatedList(res.data.recon.subdomains.consolidated);
                setConsolidatedNewList(res.data.recon.subdomains.consolidatedNew);
                setLoaded(true);
            })
            .catch(err=>console.log(err))
    }, [props.thisFqdn._id, refresh])
    
    const buildConsolidatedList = (sublist3r, amass, assetfinder, gau) => {
        let consolidated = [];
        for (let i=0; i<sublist3r.length; i++){
            if (!consolidated.includes(sublist3r[i])){
                consolidated.push(sublist3r[i]);
            }
        }
        for (let i=0; i<amass.length; i++){
            if (!consolidated.includes(amass[i])){
                consolidated.push(amass[i]);
            }
        }
        for (let i=0; i<assetfinder.length; i++){
            if (!consolidated.includes(assetfinder[i])){
                consolidated.push(assetfinder[i]);
            }
        }
        for (let i=0; i<gau.length; i++){
            if (!consolidated.includes(gau[i])){
                consolidated.push(gau[i]);
            }
        }
        setConsolidatedList(consolidatedNewList);
        setConsolidatedNewList(consolidated);
        setLoaded(true);
        let tempFqdn = props.thisFqdn;
        tempFqdn.recon.subdomains.consolidated = consolidatedNewList;
        tempFqdn.recon.subdomains.consolidatedNew = consolidated;
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{let temp = refresh + 1; setRefresh(temp); console.log(res);})
            .catch(err=>console.log(err))
    }
    
    const consolidate = () => {
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                buildConsolidatedList(res.data.recon.subdomains.sublist3r, res.data.recon.subdomains.amass, res.data.recon.subdomains.assetfinder, res.data.recon.subdomains.gau);
            })
            .catch(err=>console.log(err));
    }

    const copyListToClipboard = (e) => {
        let copyString = "";
        consolidatedList.map((fqdn, i)=>{
            return (copyString += fqdn + "\n")
        })
        navigator.clipboard.writeText(copyString);
        addToast(`Consolidated List copied to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    const copyToClipboard = e => {
        navigator.clipboard.writeText(e.target.innerText)
        addToast(`Copied "${e.target.innerText}" to Clipboard`, {appearance:'info',autoDismiss:true});
    }

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <p>This tool will consolidate any lists of subdomains that have been uploaded through the tools above.  Click the button below and a comprehensive list of all unique subdomains will be dynamically renderred.  This can take some time depending on the size of the lists, so please be patient.</p>
                    <p>After running the tool, paste the list in a newly created file using the following command: <span onClick={copyToClipboard}>vim consolidated.{props.thisFqdn.fqdn}.txt</span></p>
                    <button className="btn btn-primary" onClick={consolidate}>Consolidate</button>
                </div>
            </div>
            <div className="row mt-5">
                <div style={{width: '400px', height: '500px', overflowY: 'scroll', border: '1px solid black'}}className="col-5 ml-5">
                    <button className="btn btn-primary mt-3 btn-sm float-right" onClick={copyListToClipboard}>Copy</button>
                    <h5 className="mt-3">Consolidated List ({consolidatedList.length})</h5>
                    <hr className="mt-3 mb-1"/>
                    { loaded === true ?
                        consolidatedList.map((subdomain, i)=>{
                            return (<p className="mb-1" key={i}>{subdomain}</p>)
                        }) :
                        ''
                    }
                </div>
                <div style={{width: '400px', height: '500px', overflowY: 'scroll', border: '1px solid black'}}className="col-5 ml-5">
                    <button className="btn btn-primary mt-3 btn-sm float-right" onClick={copyListToClipboard}>Copy</button>
                    <h5 className="mt-3">New Subdomains ({consolidatedNewList.length})</h5>
                    <hr className="mt-3 mb-1"/>
                    { loaded === true ?
                        consolidatedNewList.map((subdomain, i)=>{
                            return (<p className="mb-1" key={i}>{subdomain}</p>)
                        }) :
                        ''
                    }
                </div>
            </div>
        </div>
    )
}

export default Consolidator;