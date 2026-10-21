// LAYOUTFORSLAG (midlertidig, bare på testadressen): ?tema=1..4 velger forslag, ?tema=0 er dagens side.
// Valget huskes mens man klikker rundt på siden.
(function () {
  const fraUrl = new URLSearchParams(location.search).get('tema');
  let tema = '1';
  try {
    if (fraUrl !== null) sessionStorage.setItem('tema', fraUrl);
    tema = sessionStorage.getItem('tema') ?? '1';
  } catch (e) { if (fraUrl !== null) tema = fraUrl; }
  if (!/^[0-4]$/.test(tema)) tema = '1';
  if (tema !== '0') {
    for (const fil of ['mork-felles.css', 'tema-' + tema + '.css']) {
      document.write('<link rel="stylesheet" href="/assets/forslag/' + fil + '">');
    }
  } else {
    document.write('<link rel="stylesheet" href="/assets/forslag/mork-felles.css" media="not all">');
  }
  const navn = ['Dagens', '1 Natt', '2 Overgang', '3 Grafitt', '4 Arbeidstegning'];
  document.addEventListener('DOMContentLoaded', () => {
    const v = document.createElement('div');
    v.className = 'forslag-velger';
    v.innerHTML = '<span>Forslag:</span>' + navn.map((n, i) =>
      `<a href="?tema=${i}"${String(i) === tema ? ' aria-current="true"' : ''}>${n}</a>`).join('');
    document.body.appendChild(v);
  });
})();
