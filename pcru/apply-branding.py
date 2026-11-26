"""Apply PCRU branding to the hbb_common submodule (run after checkout, before build)."""
import re, pathlib

APP_NAME = "PCRU Remote"
SERVER = "172.16.10.17"
PUB_KEY = "1pQ+vSLlfQuqjO0L1CoRdiLca7e1B32aC38CtpbZxOw="  # public key only

p = pathlib.Path("libs/hbb_common/src/config.rs")
s = p.read_text(encoding="utf-8")
s, n1 = re.subn(r'RwLock::new\("RustDesk"\.to_owned\(\)\)', f'RwLock::new("{APP_NAME}".to_owned())', s)
s, n2 = re.subn(r'RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];', f'RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"];', s)
s, n3 = re.subn(r'RS_PUB_KEY: &str = "[^"]*";', f'RS_PUB_KEY: &str = "{PUB_KEY}";', s)
# Pre-fill the options shown in Settings > Network, so the UI treats this as a private server
defaults = (
    'RwLock::new(HashMap::from(['
    f'("custom-rendezvous-server".to_owned(), "{SERVER}".to_owned()), '
    f'("relay-server".to_owned(), "{SERVER}".to_owned()), '
    f'("key".to_owned(), "{PUB_KEY}".to_owned())'
    ']));'
)
s, n4 = re.subn(r'(DEFAULT_SETTINGS: RwLock<HashMap<String, String>> = )Default::default\(\);',
                lambda m: m.group(1) + defaults, s)
assert (n1, n2, n3, n4) == (1, 1, 1, 1), (n1, n2, n3, n4)
p.write_text(s, encoding="utf-8")
print("branding applied:", APP_NAME, SERVER)
