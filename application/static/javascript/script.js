function delete_recipe() {
    event.preventDefault()
    let del = document.querySelector(".title-name").innerHTML

    return fetch(`/recipes/${del}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url
            }
        })
}


function update() {
    event.preventDefault()
    let req_body = new FormData()
    let update = document.querySelector(".title-name").innerHTML
    update = update.slice(6)
    req_body.append("Recipe Name", document.querySelector('[name="Recipe Name"]').value)
    req_body.append("Recipe Keyword", document.querySelector('[name="Recipe Keyword"]').value)
    req_body.append("Recipe Ingredients", document.querySelector('[name="Recipe Ingredients"]').value)
    req_body.append("Recipe Instructions", document.querySelector('[name="Recipe Instructions"]').value)
    return fetch(`/update/${update}`, {
            method: 'PUT',
            body: req_body
        })
        .then(respone => {
            if (respone.redirected) {
                window.location.href = respone.url
            }
        })
}
