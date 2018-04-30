const Modal = (function () {
    const editButton = document.getElementById('edit-button');

    /**
     * Abre el modal
     **/
    function open($modal, section, p) {
        const editTitle = document.getElementById('edit-title');
        const saveTitle = document.getElementById('save-title');
        const saveButton = document.getElementById('save-button');

        const saveSection = document.getElementById('save-section')
        const editSection = document.getElementById('edit-section')

        $modal.classList.add('is-active');

        if (section === 'add') {
            editButton.classList.add('is-hidden');
            editTitle.classList.add('is-hidden');
            editSection.classList.add('is-hidden')

            saveButton.classList.remove('is-hidden');
            saveTitle.classList.remove('is-hidden');
            saveSection.classList.remove('is-hidden')
        } else if (section === 'edit') {
            saveButton.classList.add('is-hidden');
            saveTitle.classList.add('is-hidden');
            saveSection.classList.add('is-hidden')

            editButton.classList.remove('is-hidden');
            editTitle.classList.remove('is-hidden');
            editSection.classList.remove('is-hidden')

            let productId = document.getElementById('product-id')
                .value = p.id
            let productName = document.getElementById('product-name')
                .value = p.name
            let productPrice = document.getElementById('product-price')
                .value = p.price
            let productQuantity = document.getElementById('product-quantity')
                .value = p.quantity
        }  
    }

    /**
     * Cierra el modal
     **/
    function close($modal) {
        $modal.classList.remove('is-active');

        if (!editButton.disabled) {
            editButton.disabled = true
        }
    }

    /**
     * Inicializa el modal de agregar producto
     **/
    function init(config) {
        const $modal = document.querySelector(config.el);

        // Inicializamos el select de productos
        Select.init({
            el: '#select',
            data: config.products,
            onSelect: config.onProductSelect
        });

        // Nos ponemos a escuchar cambios en el input de cantidad
        $modal.querySelector('#quantity')
            .addEventListener('input', function () {
                config.onChangeQunatity(this.value)
            });

        $modal.querySelector('#save-button')
            .addEventListener('click', config.onAddProduct);


        function enableEditButton() {
            editButton.disabled = false
        }

        $modal.querySelector('#edit-section')
            .addEventListener('input', enableEditButton);

        editButton.addEventListener('click', function() {
                let pid = document.getElementById('product-id').value
                config.onEditProduct(pid)
            });

        return {
            close: close.bind(null, $modal),
            open: open.bind(null, $modal)
        }
    }

    return {
        init
    }
})();

