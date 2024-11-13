import toast, { Toaster } from 'react-hot-toast';

const Slackbot = props => {


    const notify = e => {
        navigator.clipboard.writeText(e.target.innerText)
        toast(`Copied "${e.target.innerText}" to Clipboard`)
    }



    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-12">
                    <Toaster />
                    <p><b>DETAILS: </b>Sublert is a security and reconnaissance tool which leverages certificate transparency to automatically monitor new subdomains deployed by specific organizations and issued TLS/SSL certificate.</p>
                    <p><b>GOAL: </b>Configure a Virtual Private Server (VPS) to notify, via Slack, when an organization is issued a new TLS/SSL certificate.</p>
                    <p><b>DOWNLOAD / INSTALL: </b><span onClick={notify}>sudo git clone https://github.com/yassineaboukir/sublert.git && cd sublert; sudo pip3 install virtualenv setuptools; virtualenv sublert; source sublert/bin/activate; sudo pip3 install -r requirements.txt;</span></p>
                    <p><b>RUN: </b> Detailed information on configuring Slack and Cron to run this tool can be found <a href="https://medium.com/@yassineaboukir/automated-monitoring-of-subdomains-for-fun-and-profit-release-of-sublert-634cfc5d7708" target="_blank" rel="noreferrer">here</a></p>
                </div>
            </div>
        </div>
    )
}

export default Slackbot;