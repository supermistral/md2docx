import { load as loadYaml } from "js-yaml";


export const findFrontmatter = (text: string) => {
    const regexp = /(?<=^-{3}\n|\n\n-{3}\n)[^\n][\w\W]+?(?=-{3}\n|\.{3}\n)/
    const matches = regexp.exec(text);

    if (matches === null) {
        return null;
    }

    return matches[0];
}


export const parseFrontmatter = (text: string) => {
    const frontmatterText = findFrontmatter(text);

    if (frontmatterText === null) {
        return null;
    }

    try {
        return loadYaml(frontmatterText);
    } catch (e) {
        console.log(e);
    }

    return null;
}


export const findBlockMetadata = (text: string) => {
    const regexp = / {(.+)}$/gm
    const matches = [...text.matchAll(regexp)];

    if (matches.length === 0) {
        return null;
    }

    return matches;
}