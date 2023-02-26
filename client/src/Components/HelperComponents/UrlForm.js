import React, {useState, useEffect} from 'react';
import axios from 'axios';

const UrlForm = props => {
    const [url, setUrl] = useState("");
    const [urlList, setUrlList] = useState([]);
    const [loaded, setLoaded] = useState(false);

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                console.log(res.data)
                setUrlList(res.data.targetUrls);
                setLoaded(true);
            })
            .catch(err=>console.log(err))
    }, [props.thisFqdn, props.thisScanner])
    
    const handleSubmit = (e) => {
        e.preventDefault();
        let newUrl = url;
        if (newUrl.slice(-1) === "/"){
            newUrl = newUrl.substring(0, newUrl.length - 1);
        }
        let data = {};
        let currentUrls = urlList;
        currentUrls.push(newUrl);
        data["_id"] = props.thisFqdn._id;
        data["targetUrls"] = currentUrls;
        console.log(data);
        axios.post('http://localhost:8000/api/fqdn/update', data)
            .then(res=>{
                axios.post('http://localhost:8000/api/url/new', {url:newUrl, fqdn:props.thisFqdn.fqdn})
                    .then(res=>{
                        console.log(res.data);
                        setLoaded(false);
                        setUrl("");
                        setUrlList(currentUrls);
                        setLoaded(true);
                    })
                    .catch(err=>console.log(err));
            })
            .catch(err=>console.log(err));
    }

    const deleteUrl = (index) => {
        setLoaded(false);
        let data = {};
        let urlToDelete = urlList.filter((url, i) => {
            return i === index
        });
        let currentUrls = urlList.filter((url, i) => {
            return i !== index
        });
        data["_id"] = props.thisFqdn._id;
        data["targetUrls"] = currentUrls;
        console.log(data);
        axios.post('http://localhost:8000/api/fqdn/update', data)
            .then(res=>{
                axios.post('http://localhost:8000/api/url/auto/delete', {url: urlToDelete})
                    .then(res=>{
                        setUrlList(currentUrls)
                        console.log(res);
                        setLoaded(true);
                    })
                    .catch(err=>console.log(err));
            })
            .catch(err=>console.log(err));
    }

    return (
                <>
                <div className="col-12 mt-4">
                    <div style={{padding: '10px', height: '300px', width: '1000px', overflowY: 'scroll', border: '1px solid black'}}>
                        {
                            loaded && urlList.map((url, i)=>{
                                return(
                                    <p key={i}><button className="btn btn-primary mr-4" onClick={(e)=>deleteUrl(i)}>Delete</button>{url}</p>
                                )
                            })
                        }
                    </div>
                </div>
                <div className="col-12 mt-3 ml-5">
                    <form onSubmit={handleSubmit}>
                    <div className="col-10">
                        <label htmlFor="targetUrl" className="form-label">Target URL</label>
                        <input value={url} type="text" className="form-control" id="targetUrl" aria-describedby="targetUrlSubtext" onChange={(e)=>setUrl(e.target.value)} />
                    </div>
                    <div className="col-2 mt-2">
                        <button type="submit" className="btn btn-primary">Submit</button>
                    </div>
                    </form>
                </div>
                </>
    )
}

export default UrlForm;