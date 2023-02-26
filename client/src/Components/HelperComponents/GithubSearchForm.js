import React, {useState} from 'react';
import axios from 'axios';

const GithubSearchForm = props => {
    const [formData, setformData] = useState([]);

    const handleSubmit = (e) => {
        e.preventDefault();
        const resultsArray = formData.split("\n");
        let finalArr = [];
        for (const search of resultsArray){
            const tempArr = search.split("|");
            const tempObj = {"payload":tempArr[0], "results":tempArr[1], "url":tempArr[2]}
            finalArr.push(tempObj);
        }
        let tempFqdn = props.thisFqdn;
        tempFqdn.recon.osint.GithubSearch = finalArr;
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>{
                props.thisFormCompleted(true);
            })
            .catch(err=>console.log(err))
    }
    
    return (
        <div className="row mt-5">
            <div className="col-12">
                <form className="form-floating ml-3" onSubmit={handleSubmit}>
                    <label>Paste contents of brutedork.{props.thisFqdn.fqdn}.txt here:</label>
                    <textarea className="form-control" style={{height:"300px", width:"1100px"}} placeholder="example.com&#x0a;dev.example.com&#x0a;beta.example.com&#x0a;..." onChange={(e)=>setformData(e.target.value)}></textarea>
                    <button className="btn btn-primary mt-2" type="submit">Add Subdomains</button>
                </form>
            </div>
        </div>
    )
}

export default GithubSearchForm