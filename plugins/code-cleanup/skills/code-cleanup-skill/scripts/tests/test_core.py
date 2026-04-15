"""单元测试：code-cleanup 核心分析函数"""
import sys
import unittest
from pathlib import Path

# 将脚本目录添加到 path
SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_cleanup_candidates import (
    has_import_reference,
    non_self_reference_hits,
    extract_component_tag_name,
    extract_name_variants,
    infer_history_file,
    pick_risk,
    _is_default_keep,
    _is_path_keyword,
    find_weak_mentions,
)


class TestExtractComponentTagName(unittest.TestCase):
    def test_pascal_case(self):
        assert extract_component_tag_name(Path("MyButton.vue")) == "my-button"

    def test_camel_case(self):
        assert extract_component_tag_name(Path("myButton.vue")) == "my-button"

    def test_single_word(self):
        assert extract_component_tag_name(Path("Button.vue")) == "button"

    def test_already_kebab(self):
        assert extract_component_tag_name(Path("my-button.vue")) == "my-button"

    def test_with_underscore(self):
        assert extract_component_tag_name(Path("my_button.vue")) == "my-button"

    def test_multi_word_pascal(self):
        assert extract_component_tag_name(Path("MyCourseItem.vue")) == "my-course-item"


class TestExtractNameVariants(unittest.TestCase):
    def test_pascal_case_generates_all_variants(self):
        variants = extract_name_variants(Path("MyButton.vue"))
        assert "MyButton" in variants       # PascalCase
        assert "my-button" in variants       # kebab-case
        assert "my_button" in variants       # snake_case
        assert "MyButton.vue" in variants    # full filename

    def test_single_word(self):
        variants = extract_name_variants(Path("login.js"))
        assert "login" in variants
        assert "login.js" in variants

    def test_already_kebab(self):
        variants = extract_name_variants(Path("my-button.vue"))
        assert "my-button" in variants
        assert "MyButton" not in variants  # my-button 不是 PascalCase，不需要转


class TestHasImportReference(unittest.TestCase):
    def test_js_import_from(self):
        text = 'import { Button } from "./components/Button"'
        assert has_import_reference(text, "Button", ".js") is True

    def test_js_import_not_found(self):
        text = 'import { Input } from "./components/Input"'
        assert has_import_reference(text, "Button", ".js") is False

    def test_js_require(self):
        text = 'const utils = require("./utils/helper")'
        assert has_import_reference(text, "helper", ".js") is True

    def test_js_dynamic_import(self):
        text = "const mod = import('./modules/feature')"
        assert has_import_reference(text, "feature", ".js") is True

    def test_python_import(self):
        text = "import my_module"
        assert has_import_reference(text, "my_module", ".py") is True

    def test_python_from_import(self):
        text = "from my_package import my_func"
        assert has_import_reference(text, "my_func", ".py") is True

    def test_go_import(self):
        text = 'import "fmt"'
        assert has_import_reference(text, "fmt", ".go") is True

    def test_java_import(self):
        text = "import com.example.MyClass;"
        assert has_import_reference(text, "MyClass", ".java") is True

    def test_rust_use(self):
        text = "use std::collections::HashMap;"
        assert has_import_reference(text, "HashMap", ".rs") is True

    def test_unknown_ext_fallback(self):
        text = "some random text with mymodule in it"
        assert has_import_reference(text, "mymodule", ".unknown") is True

    def test_keyword_in_comment_near_import(self):
        """关键词在 import 附近的注释中不应误匹配（200字符窗口内的已知限制）"""
        text = "import { SomethingElse } from './other'\n// Button is a component"
        # 当前的实现可能匹配也可能不匹配，取决于窗口
        # 这个测试记录了当前行为
        result = has_import_reference(text, "Button", ".js")
        # Button 出现在 import 后200字符内，但不跟在引号后面
        # 由于 import pattern 匹配了 from './other'，Button 在后续200字符内
        # 这是一个已知的精度限制


class TestInferHistoryFile(unittest.TestCase):
    def test_copy_suffix(self):
        assert infer_history_file(Path("login-copy.js")) is True

    def test_bf_suffix(self):
        assert infer_history_file(Path("page-bf.vue")) is True

    def test_old_suffix(self):
        assert infer_history_file(Path("component-old.ts")) is True

    def test_bak_patterns(self):
        assert infer_history_file(Path("file_bak.js")) is True
        assert infer_history_file(Path("file.bak.js")) is True

    def test_normal_file(self):
        assert infer_history_file(Path("login.js")) is False

    def test_chinese_backup(self):
        assert infer_history_file(Path("文件备份.txt")) is True


class TestPickRisk(unittest.TestCase):
    def test_high_risk(self):
        assert pick_risk([]) == "high"

    def test_medium_risk_with_weak(self):
        assert pick_risk(["存在弱引用线索"]) == "medium"

    def test_low_risk_history_only(self):
        assert pick_risk([], history_pattern_hit=True) == "low"


class TestIsDefaultKeep(unittest.TestCase):
    def test_entry_files(self):
        assert _is_default_keep("src/main.js") is True
        assert _is_default_keep("src/App.vue") is True
        assert _is_default_keep("src/__init__.py") is True

    def test_config_files(self):
        assert _is_default_keep("vite.config.js") is True
        assert _is_default_keep("webpack.config.ts") is True

    def test_router_files(self):
        assert _is_default_keep("src/router.js") is True
        assert _is_default_keep("src/routes.ts") is True

    def test_test_files(self):
        assert _is_default_keep("src/utils/test.js") is False  # test 是文件名，不是 *.test.*
        assert _is_default_keep("src/utils/format.test.js") is True

    def test_test_directory(self):
        assert _is_default_keep("src/__tests__/format.js") is True

    def test_normal_file(self):
        assert _is_default_keep("src/components/Button.vue") is False


class TestIsPathKeyword(unittest.TestCase):
    def test_path_like(self):
        assert _is_path_keyword("src/utils/helper") is True

    def test_filename_like(self):
        assert _is_path_keyword("helper.js") is True

    def test_plain_keyword(self):
        assert _is_path_keyword("helper") is False

    def test_backslash(self):
        assert _is_path_keyword("src\\utils") is True


class TestFindWeakMentions(unittest.TestCase):
    def test_string_path_mention(self):
        """路径片段引用：/token/ 形式"""
        pool = {"other.js": "const path = '/login/'"}
        hits = find_weak_mentions("target.js", pool, "login")
        assert len(hits) > 0

    def test_dash_mention(self):
        """动态导入中的引用"""
        pool = {"other.js": "import('./my-button')"}
        hits = find_weak_mentions("target.js", pool, "my-button")
        assert len(hits) > 0

    def test_template_tag_usage(self):
        """B4: 模板标签引用 <my-button> 现在可以检测"""
        pool = {"other.vue": '<template><my-button>Click</my-button></template>'}
        hits = find_weak_mentions("target.vue", pool, "my-button")
        assert len(hits) > 0

    def test_closing_tag(self):
        """闭合标签 </my-button>"""
        pool = {"other.vue": '</my-button>'}
        hits = find_weak_mentions("target.vue", pool, "my-button")
        assert len(hits) > 0

    def test_path_usage(self):
        """路由配置中的路径引用"""
        pool = {"router.js": "routes.push({ path: '/login/' })"}
        hits = find_weak_mentions("target.js", pool, "login")
        assert len(hits) > 0

    def test_route_config_mention(self):
        """路由配置属性引用"""
        pool = {"router.js": "component: 'LoginPage'"}
        hits = find_weak_mentions("target.js", pool, "LoginPage")
        assert len(hits) > 0

    def test_string_literal_mention(self):
        """字符串字面量引用"""
        pool = {"other.js": "const name = 'myModule'"}
        hits = find_weak_mentions("target.js", pool, "myModule")
        assert len(hits) > 0

    def test_no_mentions(self):
        pool = {"other.js": "const x = 42"}
        hits = find_weak_mentions("target.js", pool, "nonexistent")
        assert len(hits) == 0

    def test_self_excluded(self):
        pool = {"target.js": "'/login/' is here"}
        hits = find_weak_mentions("target.js", pool, "login")
        assert len(hits) == 0


class TestNonSelfReferenceHits(unittest.TestCase):
    def test_finds_reference(self):
        pool = {
            "src/utils/helper.js": "export function helper() {}",
            "src/page/main.js": 'import { helper } from "../utils/helper.js"',
        }
        hits = non_self_reference_hits("src/utils/helper.js", pool, ["helper"])
        assert "src/page/main.js" in hits

    def test_excludes_self(self):
        pool = {
            "src/utils/helper.js": "import { helper } from '../utils/helper.js'",
        }
        hits = non_self_reference_hits("src/utils/helper.js", pool, ["helper"])
        assert len(hits) == 0

    def test_no_reference(self):
        pool = {
            "src/utils/dead.js": "export function dead() {}",
            "src/page/main.js": 'import { helper } from "../utils/helper.js"',
        }
        hits = non_self_reference_hits("src/utils/dead.js", pool, ["dead"])
        assert len(hits) == 0
