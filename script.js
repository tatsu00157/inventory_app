/* script.js */
document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    const postTable = document.getElementById("post-table"); // テーブルのIDを指定
    const noResultsMessage = document.getElementById("no-results-message"); // メッセージ要素
    
    searchButton.addEventListener("click", function() {
        const query = searchInput.value.toLowerCase();

        // テーブル内の全ての行を取得
        const rows = document.querySelectorAll("#post-table tbody tr");
        const headerCells = document.querySelectorAll(".header-cell"); // ヘッダー行のセル
        let noResults = true; // 検索結果が見つからない場合を示すフラグ

        // 一番上のヘッダーセルは表示し、他のヘッダーセルは非表示にする
        headerCells.forEach(function(cell) {
            cell.style.display = ""; // ヘッダーセルを表示
        });

        rows.forEach(function(row) {
            const titleCell = row.querySelector(".title-cell"); // セルを行内で検索
            if (titleCell) {
                const title = titleCell.textContent.toLowerCase();

                if (title.includes(query)) {
                    row.style.display = ""; // 一致する場合、行を表示
                    noResults = false; // 一致するデータが見つかった場合、フラグをfalseに設定
                } else {
                    row.style.display = "none"; // 一致しない場合、行を非表示
                }
            }
            
        });
        // 検索結果が見つからなかった場合、メッセージを表示
        if (noResults) {
            noResultsMessage.style.display = "block";
        } else {
            noResultsMessage.style.display = "none";
        }
    });
    // 商品の増減を非同期で処理
    postTable.addEventListener("click", function(event) {
        if (event.target.tagName === "A") {
            event.preventDefault();
            const post_id = event.target.getAttribute("data-post-id");
            const action = event.target.getAttribute("data-action");

            if (post_id && action) {
                updateQuantity(post_id, action);
            }
        }
    });
    function updateQuantity(post_id, action) {
        // Ajaxリクエストを作成
        const xhr = new XMLHttpRequest();
        xhr.open("GET", `/update_quantity/${post_id}/${action}`, true);

        // リクエスト完了時の処理
        xhr.onload = function() {
            if (xhr.status === 200) {
                // 在庫数を非同期で更新
                const quantityElement = document.getElementById(`quantity-${post_id}`);
                const newQuantity = parseInt(quantityElement.textContent) + (action === "increment" ? 1 : -1);
                quantityElement.textContent = newQuantity;
            }
        };
         // リクエストを送信
         xhr.send();
        }
    });
