import React, {Component, PropTypes} from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {EditIcon, TagIcon} from 'src/components/bases/icons'

import MemoComponent from 'src/components/commons/MemoComponent'


/**
 * メタデータエリア(編集可能)
 */
class MetadataEditablePaper extends Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    editDisabled: PropTypes.bool,
    onEditTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
      editDisabled = false,
      onEditTouchTap,
    } = this.props

    const style = {
      root: {
        display: 'flex',
        flexFlow: 'row nowrap',
        padding: 24,
      },

      contents: {
        display: 'flex',
        flexFlow: 'column nowrap',
      },

      tagsSection: {
      },
      tags: {
        display: 'flex',
        flexFlow: 'row wrap',
        marginLeft: -8,
        fontSize: 14,
        lineHeight: 1.1,
      },
      tag: {
        paddingLeft: 8,
      },

      memoSection: {
        paddingTop: 16,
      },
      memo: {
        fontSize: 14,
        lineHeight: 1.1,
      },
    }

    return (
      <Paper>
        <div style={style.root}>
          <ComponentWithIconButton
            icon={EditIcon}
            iconButtonDisabled={editDisabled}
            onIconButtonTouchTap={onEditTouchTap}
          >
            <div style={style.contents}>
              <div style={style.tagsSection}>
                <ComponentWithSubTitle subTitle="タグ" icon={TagIcon}>
                  <div style={style.tags}>
                    {module.tags.valueSeq().map((tag, index) =>
                      <span key={index} style={style.tag}>{tag}</span>
                    )}
                  </div>
                </ComponentWithSubTitle>
              </div>

              <div style={style.memoSection}>
                <MemoComponent obj={module} />
              </div>
            </div>
          </ComponentWithIconButton>
        </div>
      </Paper>
    )
  }
}


export default MetadataEditablePaper
