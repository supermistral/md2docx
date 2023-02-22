import { Root, Content, Parent } from "mdast"
import { findBlockMetadata, findFrontmatter } from "./utils";


const toRemarkFilter = (filter: (tree: any, text: any) => void) => () => filter;


const frontmatterFilter = (tree: Root, text: string) => {
    const frontmatter = findFrontmatter(text);

    if (frontmatter === null) {
        return;
    }

    const frontmatterWithoutSpaces = frontmatter.replaceAll(' ', '');

    let index: number, child: Content;
    let foundChildIndex = -1;

    for (let i = 0; i < tree.children.length; ++i) {
        child = tree.children[i];
        if (
            child.type === "paragraph" && 
            child.children.length === 1  && 
            child.children[0].type === "text"
        ) {
            index = child.children[0].value.replaceAll(' ', '').indexOf(frontmatterWithoutSpaces);
            if (index === 0) {
                foundChildIndex = i;
                break;
            }
        }
    }

    if (foundChildIndex === -1) {
        return;
    }

    let indicesToDelete = [foundChildIndex - 1];

    for (let i = foundChildIndex; i < tree.children.length; ++i) {
        indicesToDelete.push(i);
        child = tree.children[i];
        if (
            child.type === "paragraph" && 
            child.children.length === 1  && 
            child.children[0].type === "text"
        ) {
            const value = child.children[0].value;
            if (value.endsWith("...") || value.endsWith("---")) {
                break;
            }
        }
    }

    indicesToDelete.forEach((index, i) => tree.children.splice(index - i, 1));
}


export const remarkFrontmatterFilter = toRemarkFilter(frontmatterFilter);


const blockMetadataFilter = (element: Content, text: string) => {
    if (element.type === "text") {
        const metadataString = findBlockMetadata(element.value);
        if (metadataString !== null) {
            metadataString.forEach(metadata => {
                element.value = element.value.replace(metadata[0], "");
            })
        }
    }

    if ('children' in element) {
        for (const child of element.children) {
            blockMetadataFilter(child, text);
        }
    }
}


export const remarkBlockMetadataFilter = toRemarkFilter(blockMetadataFilter);