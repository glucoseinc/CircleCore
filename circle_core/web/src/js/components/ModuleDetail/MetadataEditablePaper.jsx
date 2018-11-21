import PropTypes from 'prop-types'
import React from 'react'

import Paper from 'material-ui/Paper'

import ComponentWithIconButton from 'src/components/bases/ComponentWithIconButton'
import ComponentWithSubTitle from 'src/components/bases/ComponentWithSubTitle'
import {AttributeIcon, EditIcon, TagIcon} from 'src/components/bases/icons'

import MemoComponent from 'src/components/commons/MemoComponent'

import ModuleAttributesTable from './ModuleAttributesTable'


/**
 * メタデータエリア(編集可能)
 */
class MetadataEditablePaper extends React.Component {
  static propTypes = {
    module: PropTypes.object.isRequired,
    onEditTouchTap: PropTypes.func,
  }

  /**
   * @override
   */
  render() {
    const {
      module,
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

      attributesSection: {
        paddingTop: 16,
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

              <div style={style.attributesSection}>
                <ComponentWithSubTitle subTitle="属性" icon={AttributeIcon}>
                  <ModuleAttributesTable module={module} />
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
