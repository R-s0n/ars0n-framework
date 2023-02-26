import React, {useState, useEffect} from 'react';
import axios from 'axios';

const GithubSearchResults = props => {
    const [searchResults, setSearchResults] = useState([]);
    const [loaded, setLoaded] = useState(false);

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                setSearchResults(res.data.recon.osint.GithubSearch);
                setLoaded(true);
            })
            .catch(err=>console.log(err))
    }, [props.thisFqdn._id])

    const deleteSubdomains = (e) => {
        let tempFqdn = props.thisFqdn;
        tempFqdn.recon.osint.GithubSearch = [];
        axios.post('http://localhost:8000/api/fqdn/update', tempFqdn)
            .then(res=>props.thisFormCompleted(false))
            .catch(err=>console.log(err))
    }

    const resultsStyle = {
        height: '400px',
        width: '1000px',
        overflowY: 'scroll',
        border: '1px solid black',
        padding: '10px'
    }

    return (
        <div className="row mt-1">
            <div className="col-12">
                <h5>Results:</h5>
                <div style={resultsStyle}>
                {
                    loaded === true ?
                    searchResults.map((search, i)=>{
                        return (
                            <div key={i} style={{marginBottom:'1px', marginLeft:'15px'}}>
                                <p className="m-0">Payload: {search.payload}</p>
                                <p className="m-0">Result Count: {search.results}</p>
                                <p className="m-0 mb-3">Link: <a href={search.url} target="_blank" rel="noreferrer">{search.url}</a></p>
                            </div>
                        )
                    }) :
                    ''
                }
                </div>
            </div>
            <div className="col-4 mt-2">
                <button className="btn btn-primary" onClick={deleteSubdomains}>Delete</button>
            </div>
        </div>
    )
}

export default GithubSearchResults;