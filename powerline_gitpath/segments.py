#     This file is part of powerline-gitpath.
#
#     powerline-gitpath is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     powerline-gitpath is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with powerline-gitpath.  If not, see <https://www.gnu.org/licenses/>.


from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info, requires_filesystem_watcher

@requires_filesystem_watcher
@requires_segment_info
class CustomSegment(Segment):
  divider_highlight_group = None

  def __call__(self, pl, segment_info, create_watcher):
    return [{
      'contents': 'hello',
      'highlight_groups': ['information:regular'],
      }]

gitpath = with_docstring(CustomSegment(), '''Return a custom segment.''')