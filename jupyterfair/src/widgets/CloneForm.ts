// import { TranslationBundle } from '@jupyterlab/translation';
import { Widget } from '@lumino/widgets';

/**
 * The UI for the form fields shown within the Clone modal.
 */



export class FairlyCloneForm extends Widget {
  /**
   * Create a redirect form.
   * @param translator - The language translator
   */
   constructor() {
    super({ node: FairlyCloneForm.createFormNode() });
  }

  /**
   * Returns the input value.
   */
  getValue(): string {
    // TODO: this shoudl be properly initialized, 
    // See: https://stackoverflow.com/questions/40349987/how-to-suppress-error-ts2533-object-is-possibly-null-or-undefined
    return encodeURIComponent(this.node.querySelector('input').value.trim()); // strickNullChecks = true brakes this code
  }

  private static createFormNode(): HTMLElement {
    const node = document.createElement('div');
    const label = document.createElement('label');
    // const label2 = document.createElement('label');
    const input = document.createElement('input');
    // const input2 = document.createElement('input');
    const text = document.createElement('span');
    // const text2 = document.createElement('span');

    node.className = 'jp-RedirectForm';
    text.textContent = 'Enter the URL or DOI of the dataset';
    // text2.textContent = 'Enter something else';
    input.placeholder = 'https://doi.org/xx.xxxx/xxxxxx.vx';
    // input2.placeholder = 'djsdasfn';

    label.appendChild(text);
    label.appendChild(input);
    node.appendChild(label);

    // label.appendChild(text2);
    // label.appendChild(input2);
    // node.appendChild(label2);
    return node;
  }
}
