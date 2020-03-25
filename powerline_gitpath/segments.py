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


import copy
import os.path

from git import Repo, NoSuchPathError, InvalidGitRepositoryError
from powerline.lib.unicode import out_u
from powerline.segments import Segment, with_docstring
from powerline.theme import requires_filesystem_watcher
from powerline.theme import requires_segment_info


@requires_filesystem_watcher
@requires_segment_info
class GitPathSegment(Segment):
    def argspecobjs(self):
        for obj in super(GitPathSegment, self).argspecobjs():
            yield obj
        yield 'get_shortened_path', self.get_shortened_path

    def omitted_args(self, name, method):
        if method is self.get_shortened_path:
            return ()
        else:
            return super(GitPathSegment, self).omitted_args(name, method)
        
    def is_git(self, segment_info):
        try:
            path = segment_info['getcwd']()
            Repo(path, search_parent_directories=True)
            return True
        except InvalidGitRepositoryError:
            return False

      

    def get_shortened_path(self, pl, segment_info, path_when_outside, shorten_home=True, **kwargs):
        try:
            path = out_u(segment_info['getcwd']())
            path = segment_info['getcwd']()
            try:
                repo = Repo(path, search_parent_directories=True)
                reponame = os.path.basename(repo.working_dir)
                repopath = repo.working_dir
                path = path.replace(repopath, "", 1)
                if path == "":
                    path = os.sep
                if path.startswith(os.sep):
                    path = path[len(os.sep):]
            except InvalidGitRepositoryError as e:
                if path_when_outside:
                    path = out_u(segment_info['getcwd']())
                    if shorten_home:
                        home = segment_info['home']
                        if home:
                            home = out_u(home)
                            if path.startswith(home):
                                path = '~' + path[len(home):]
                else:
                    raise
        except OSError as e:
            if e.errno == 2:
                # user most probably deleted the directory
                # this happens when removing files from Mercurial repos for example
                pl.warn('Current directory not found')
                return '[not found]'
            else:
                raise
        return path

    def __call__(self, pl, segment_info,
                 dir_shorten_len=None,
                 dir_limit_depth=None,
                 use_path_separator=False,
                 path_when_outside=True,
                 ellipsis='...',
                 **kwargs):
        cwd = self.get_shortened_path(pl, segment_info, path_when_outside, **kwargs)
        cwd_split = cwd.split(os.sep)
        cwd_split_len = len(cwd_split)
        cwd = [i[0:dir_shorten_len] if dir_shorten_len and i else i for i in cwd_split[:-1]] + [cwd_split[-1]]
        if dir_limit_depth and cwd_split_len > dir_limit_depth + 1:
            del (cwd[0:-dir_limit_depth])
            if ellipsis is not None:
                cwd.insert(0, ellipsis)
        ret = []
        if not cwd[0] and not self.is_git(segment_info):
            cwd[0] = os.sep
        draw_inner_divider = not use_path_separator
        for part in cwd:
            if not part:
                continue
            if use_path_separator:
                part += os.sep
            ret.append({
                'contents': part,
                'highlight_groups': ['cwd'],
                'divider_highlight_group': 'cwd:divider',
                'draw_inner_divider': draw_inner_divider,
            })
        ret[-1]['highlight_groups'] = ['cwd:current_folder', 'cwd']

        if use_path_separator:
            ret[-1]['contents'] = ret[-1]['contents'][:-1]
            if len(ret) > 1 and ret[0]['contents'][0] == os.sep:
                ret[0]['contents'] = ret[0]['contents'][1:]
        return ret


gitpath = with_docstring(GitPathSegment(), '''Return a custom segment.''')


@requires_filesystem_watcher
@requires_segment_info
class GitNameSegment(Segment):
    def __call__(self, pl, segment_info, **kwargs):
        repo = Repo(segment_info['getcwd'](), search_parent_directories=True)
        reponame = os.path.basename(repo.working_dir)

        return [{
            'contents': reponame,
            'highlight_groups': ['information:regular'],
        }]


gitname = with_docstring(GitNameSegment(), '''Return name of git''')
