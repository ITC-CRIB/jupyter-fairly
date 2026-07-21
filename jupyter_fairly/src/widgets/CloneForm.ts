import { Widget } from '@lumino/widgets';

/**
 * The UI for the form fields shown within the Clone modal.
 */
export class FairlyCloneForm extends Widget {
  /**
   * Creates a form for cloning datasets
   *
   */
  constructor() {
    super({ node: FairlyCloneForm.createFormNode() });
  }

  /**
   * Returns the input value as plain text
   */
  getValue(): string {
    const input = this.node.querySelector('input');
    return input ? input.value.trim() : '';
  }

  private static createFormNode(): HTMLElement {
    const node = document.createElement('div');
    const label = document.createElement('label');
    const input = document.createElement('input');
    const text = document.createElement('span');

    node.className = 'jp-RedirectForm';
    text.textContent = 'Enter URL or DOI: ';
    input.placeholder = 'https://doi.org/xx.x/xx.vx';

    label.appendChild(text);
    label.appendChild(input);
    node.appendChild(label);
    return node;
  }
}
