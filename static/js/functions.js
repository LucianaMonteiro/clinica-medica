document.addEventListener(
    "htmx:confirm",
    function (e) {
        if (e.detail.question !== null) {
            e.preventDefault();
            Swal.fire({
                icon: 'question',
                buttonsStyling: false,
                showCancelButton: true,
                reverseButtons: true,
                title: 'Favor confirmar!',
                text: `Deseja mesmo excluir o cadastro de ${(e.detail.question).toUpperCase()}?`,
                showClass: { popup: 'animate__animated animate__fadeInUp animate_faster' },
                hideClass: { popup: 'animate__animated animate__fadeOutDown animate_faster' },
            }).then(function (res) {
                if (res.isConfirmed) e.detail.issueRequest(true)
            })
        }
    }
);

function onClick(obj) {
    let editing = document.querySelector('.editing');

    if (editing) {
        htmx.trigger(editing, 'cancel')
    } else {
        htmx.trigger(obj, 'edit')
    }
}