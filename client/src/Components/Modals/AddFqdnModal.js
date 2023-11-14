import axios from 'axios';
import React, { useState } from 'react';

const AddFqdnModal = props => {
    const [file, setFile] = useState(null);
    const [manualFqdn, setManualFqdn] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    }

    const handleManualChange = (e) => {
        setManualFqdn(e.target.value);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("handleSubmitFunctionStart");
        if (file) {
            console.log("Reading file");
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    props.setNoFqdns(false); 
                    const content = JSON.parse(e.target.result);
                    const inScope = content.target?.scope?.include;
            
                    if (Array.isArray(inScope)) {
                        // Create an initial list of domains
                        let domains = inScope.filter(inclusion => inclusion.enabled)
                                             .map(inclusion => {
                                                 // Remove protocol, www, and any special regex characters
                                                 return inclusion.host.replace(/(https?:\/\/)?(www\.)?/g, '')
                                                                      .replace(/[\^$\\]/g, '');
                                             });
    
                        // Filter out duplicates
                        domains = [...new Set(domains)];
    
                        axios.all(domains.map(domain => axios.post('http://localhost:8000/api/fqdn/new', { fqdn: domain })))
                        .then(axios.spread((...responses) => {
                            const newFqdns = responses.map(res => res.data);
                            props.setFqdns(prevFqdns => [...prevFqdns, ...newFqdns]);
            
                            // Set the first FQDN from the new list as the current FQDN
                            if (newFqdns.length > 0) {
                                props.setCurrentFqdn(newFqdns[0]);
                            }
                        }))
                        .catch(err => console.log(err));
                        }
                } catch (err) {
                    console.error("Error parsing JSON", err);
                }
            };                                  
    
            reader.readAsText(file);
        } else if (manualFqdn) {
            console.log("Manually adding...");
            props.setNoFqdns(false); 
            // Handle manual domain addition
            const domain = manualFqdn.replace(/(https?:\/\/)?(www\.)?/g, '');
            axios.post('http://localhost:8000/api/fqdn/new', { fqdn: domain })
                .then(res => {
                    const newFqdn = res.data;
                    props.setFqdns(prevFqdns => [...prevFqdns, newFqdn]);
        
                    // Set the added FQDN as the current FQDN
                    props.setCurrentFqdn(newFqdn);
                    props.setNoFqdns(false); // Call this function to close the modal
                })
                .catch(err => console.log(err));
        }
    }        
    
    

    return (
        <>
            <h1>Add FQDN</h1>
            <p>Select a Burp Suite config file or enter a FQDN manually</p>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Config File:</label>
                    <input type="file" onChange={handleFileChange} />
                </div>
                <div>
                    <label>Manual FQDN:</label>
                    <input type="text" value={manualFqdn} onChange={handleManualChange} />
                </div>
                <input type="submit" value="Add" />
            </form>
        </>
    );
}

export default AddFqdnModal;
