function showCountryExistsAlert(title) {
    swal({
        title: '<i>' + title + '</i> <u>already exists</u>',
        type: 'info',
        showCloseButton: true,
        cancelButtonClass: 'btn btn-danger ml-2',
    });
}