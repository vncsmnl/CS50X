

//Buscar Links salvos
export async function getLinksSave(key) {
    const mylinks = await localStorage.getItem(key);

    let linksSaves = JSON.parse(mylinks) || [];

    return linksSaves;
}

//Salvar um link no localStorage
export async function saveLink(key, newLink) {
    let linksStored = await getLinksSave(key);

    //Se j[a tiver um link salva com algum ID eu nao vou deixar duplicar
    const haslink = linksStored.some(link => link.id === newLink.id);

    if (haslink) {
        return;
    }

    //Adicionar esse novo link na lista (await)
    linksStored.push(newLink)
    localStorage.setItem(key, JSON.stringify(linksStored));
}

//Deletar algum item salvo.
export function deleteLink(links, id) {

    let myLinks = links.filter(item => {
        return (item.id !== id)
    })

    localStorage.setItem('@encurtaLink', JSON.stringify(myLinks));
    return myLinks;

}
