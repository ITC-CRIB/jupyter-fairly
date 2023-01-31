 
import { Widget } from '@lumino/widgets';

export class FairlyWidget extends Widget {
    constructor () {
        super();
        this.addClass('jp-example-view');
        this.id = 'fairly-widget';
        this.title.label = 'Fairly';
        this.title.closable = true;
    }
  };