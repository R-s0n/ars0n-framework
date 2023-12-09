import axios from 'axios';
import React, { useState } from 'react';

const AddFqdnModal = props => {
    const [file, setFile] = useState(null);
    const [scanFile, setScanFile] = useState(null);
    const [manualFqdn, setManualFqdn] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    }

    const handleManualChange = (e) => {
        setManualFqdn(e.target.value);
    }

    const handleScanFileChange = (e) => {
        setScanFile(e.target.files[0]);
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
                        let domains = inScope.filter(inclusion => inclusion.enabled)
                                             .map(inclusion => {
                                                 return inclusion.host.replace(/(https?:\/\/)?(www\.)?/g, '')
                                                                      .replace(/[\^$\\]/g, '');
                                             });
    
                        domains = [...new Set(domains)];
                        axios.all(domains.map(domain => axios.post('http://localhost:8000/api/fqdn/new', { fqdn: domain })))
                        .then(axios.spread((...responses) => {
                            const newFqdns = responses.map(res => res.data);
                            props.setFqdns(prevFqdns => [...prevFqdns, ...newFqdns]);
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
            const domain = manualFqdn.replace(/(https?:\/\/)?(www\.)?/g, '');
            axios.post('http://localhost:8000/api/fqdn/new', { fqdn: domain })
                .then(res => {
                    const newFqdn = res.data;
                    props.setFqdns(prevFqdns => [...prevFqdns, newFqdn]);
                    props.setNoFqdns(false); 
                })
                .catch(err => console.log(err));
        } else if (scanFile) {
            console.log(scanFile);
            console.log("Loading Scan File...")
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const importedData = JSON.parse(e.target.result);
                    importedData.forEach((importedFqdn) => {
                        const existingIndex = props.fqdns.findIndex(
                        (existingFqdn) => existingFqdn.fqdn === importedFqdn.fqdn
                        );
                        if (existingIndex === -1) {
                            props.setFqdns((prevData) => [...prevData, importedFqdn]);
                            axios.post("http://localhost:8000/api/fqdn/new",importedFqdn)
                        } else {
                            props.setFqdns((prevData) => {
                                const newData = [...prevData];
                                newData[existingIndex] = importedFqdn;
                                return newData;
                            });
                            axios.post("http://localhost:8000/api/fqdn/update",importedFqdn)
                        }
                    });
                    props.setNoFqdns(false);
                } catch (error) {
                    console.error('Error parsing JSON file:', error);
                }
            };
            reader.readAsText(scanFile);
            props.setNoFqdns(false);
            }
    }        
    
    

    return (
        <div class="container-fluid">
            <div class="container mt-5">
                <div class="text-center">
                    <h1 class="display-4">Add FQDN</h1>
                    <p class="lead">Select a Burp Suite config file or enter a FQDN manually</p>
                </div>
                <form onSubmit={handleSubmit}>
                    <div class="form-group">
                        <label for="configFile">Config File:</label>
                        <input type="file" class="form-control" id="configFile" onChange={handleFileChange} />
                    </div>
                    <div class="form-group">
                        <label for="scanFile">Scan File:</label>
                        <input type="file" class="form-control" id="scanFile" onChange={handleScanFileChange} />
                    </div>
                    <div class="form-group">
                        <label for="manualFqdn">Manual FQDN:</label>
                        <input type="text" class="form-control" id="manualFqdn" value={manualFqdn} onChange={handleManualChange} />
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg btn-block mt-5">Add</button>
                </form>
            </div>
        </div>
    );
}

export default AddFqdnModal;
