import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';
import Dashboard from '../Components/Dashboard';
import CveTesting from '../Components/CveTesting';
import Recon from '../Components/Recon';
import Enumeration from '../Components/Enumeration';
import Ops from '../Components/Ops';
import Chaining from '../Components/Chaining';
import Input from '../Components/Input';
import Bypass from '../Components/Bypass';
import Feature from '../Components/Feature';
import Creative from '../Components/Creative';


const Fqdn = props => {
    const [activeTab, setActiveTab] = useState(0);

    useEffect(()=>setActiveTab(0), [props.index]);

    const methodologyTabs = [
        "Dashboard",
        "Recon",
        "CVE Testing",
        "Enumeration",
        "Ops Testing",
        "Input Testing",
        "Bypass Testing",
        "Feature Testing",
        "Creative Testing",
        "Chaining",
        "Report"
    ]

    const deleteFqdn = () => {
        props.setActiveTab(0);
        props.buttonFunction(props.thisFqdn, props.index);
    }

    Modal.setAppElement('#root');

    return (
        <>
        <nav style={{borderBottom: '2px groove #284B63'}} className="pl-2 mb-3 navbar navbar-expand-lg bg-dark">
            <div className="container-fluid">
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-3 mb-lg-0">
                        {
                        methodologyTabs.map((tab, i) => {return (
                        <li className="mr-3 nav-item" key={i}>
                            { i === activeTab ?
                            <button style={{width: '135px'}} className="border border-info nav-link btn btn-primary text-secondary active" aria-current="page" href="#">{tab}</button> :
                            <button style={{width: '135px'}} className="border border-info nav-link btn btn-primary text-secondary" onClick={()=>setActiveTab(i)}aria-current="page" href="#">{tab}</button>
                            }
                            </li>
                        )})
                        }
                        <li><button style={{width: '135px'}} className="border border-info nav-link btn btn-primary text-secondary" onClick={deleteFqdn}>Delete</button></li>
                    </ul>
                </div>
            </div>
        </nav>
        {
            activeTab === 0 ?
            <Dashboard thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 1 ?
            <Recon thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 2 ?
            <CveTesting thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 3 ?
            <Enumeration thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 4 ?
            <Ops thisFqdn={props.thisFqdn} /> :
            ""
        }
        
        {
            activeTab === 5 ?
            <Input thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 6 ?
            <Bypass thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 7 ?
            <Feature thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 8 ?
            <Creative thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 9 ?
            <Chaining thisFqdn={props.thisFqdn} /> :
            ""
        }
        </>
    );
}

export default Fqdn;