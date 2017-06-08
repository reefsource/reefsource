import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {ActivatedRoute} from '@angular/router';
import {Store} from '@ngrx/store';
import * as fromRoot from '../../reducers';
import {Album} from '../../models/album';
import {FileUploader} from 'ng2-file-upload';
import {CookieService} from 'ngx-cookie';
@Component({
  selector: 'app-uploader',
  templateUrl: './uploader.component.html',
  styleUrls: ['./uploader.component.css']
})
export class UploaderComponent implements OnInit {

  public album$: Observable<Album>;
  public albumId: number;
  private selectedFiles: FileList;
  public uploader: FileUploader;

  @Output() itemComplete: EventEmitter<any> = new EventEmitter();

  constructor(private route: ActivatedRoute,
              private store: Store<fromRoot.State>,
              private _cookieService: CookieService) {

  }

  ngOnInit() {
    this.albumId = +this.route.params['value']['albumId'];
    this.uploader = new FileUploader({url: `/api/v1/albums/${this.albumId}/upload/`});
    this.uploader.setOptions({headers: [{name: 'X-CSRFToken', value: this._cookieService.get('csrftoken')}]});
    this.uploader.onCompleteAll = () => {
      this.itemComplete.emit();
    }
  }
}
