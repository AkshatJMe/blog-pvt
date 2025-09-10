from scripts.process_meta_images import process_notion_images
from scripts.process_notion_files import process_blog
from scripts.optimize_images import processImages
from scripts.final_transfer import transfer_to_blog
from scripts.cleanup import cleanup
from scripts.deploy_to_github import deploy_to_github
from scripts.deploy_new import deploy_public_to_gh_pages

def main():
    print("✅ Step 0: Process Raw Square and Thumb Images...")
    process_notion_images()

    print('\n')
    print("✅ Step 1: Process Notion Blogs...")
    process_blog()

    print('\n')
    print("✅ Step 2: Optimizing images...")
    processImages()

    print('\n')
    print("✅ Step 3: Transferring blog...")
    transfer_to_blog()

    print('\n')
    print("✅ Step 4: Cleanup from the above steps...")
    cleanup()

    print('\n')
    print("✅ Step 5: Deploying to GitHub...")
    deploy_public_to_gh_pages()
    # print('\n Deploy it yourself')

if __name__ == "__main__":
    main()
