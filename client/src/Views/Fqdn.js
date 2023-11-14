import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';
import Dashboard from '../Components/Dashboard';
import CveTesting from '../Components/CveTesting';
import Recon from '../Components/Recon';
import Enumeration from '../Components/Enumeration';
import Ops from '../Components/Ops';
import Chaining from '../Components/Chaining';
import Core from '../Components/Core';
import Logging from '../Components/Logging';
import Resources from '../Components/Resources';
import Creative from '../Components/Creative';
import ComingSoon from '../Components/ComingSoon';


const Fqdn = props => {
    const [activeTab, setActiveTab] = useState(0);
    useEffect(()=>setActiveTab(0), [props.index]);
    console.log("Received FQDN in Fqdn.js:", [props.thisFqdn]);

    const methodologyTabs = [
        "Dashboard",
        "Recon",
        "Enumeration",
        "CVE Testing",
        "Ops Testing",
        "Core Testing",
        "Creative Testing",
        "Chaining",
        "Report",
        "Resources",
        "Logging"
    ]

    Modal.setAppElement('#root');

    return (
        <>
        <nav style={{ borderBottom: '2px groove #284B63' }} className="pl-2 mb-3 navbar navbar-expand-lg bg-dark">
            <div className="container-fluid">
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-3 mb-lg-0">
                        {methodologyTabs.map((tab, i) => (
                            <li className="mr-3 nav-item" key={i}>
                                <button
                                    style={{ width: '135px' }}
                                    className={`border border-info nav-link btn btn-primary text-secondary ${i === activeTab ? 'active' : ''}`}
                                    onClick={() => setActiveTab(i)}
                                    aria-current="page"
                                >
                                    {tab}
                                </button>
                            </li>
                        ))}
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
            <Enumeration thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 3 ?
            <CveTesting thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 4 ?
            <Ops thisFqdn={props.thisFqdn} /> :
            ""
        }
        
        {
            activeTab === 5 ?
            <Core thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 6 ?
            <Creative thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 7 ?
            <ComingSoon thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 8 ?
            <ComingSoon thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 9 ?
            <ComingSoon thisFqdn={props.thisFqdn} /> :
            ""
        }
        {
            activeTab === 10 ?
            <Logging thisFqdn={props.thisFqdn} /> :
            ""
        }
        </>
    );
}

export default Fqdn;