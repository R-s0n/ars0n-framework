import React from 'react';

const ConfirmDeleteModal = props => {
    return (
        <>
        <h4>Delete FQDN?</h4>
        <h6>Deleting this FQDN will remove all data associated with it from the database.  This cannot be undone.  Are you sure?</h6>
        <button>Confirm</button>
        <button>Cancel</button>
        </>
    );
}

export default ConfirmDeleteModal;