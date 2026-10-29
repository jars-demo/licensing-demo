import { expect, test } from '@playwright/test'

test('home shows the index and opens chapter 01', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Whose code is it anyway?')
  const index = page.locator('section', { has: page.locator('#chapters') })
  await expect(index.locator('ol > li')).toHaveCount(8)
  await expect(index).toContainText('The copyleft two levels down')
  await expect(page.getByRole('figure').first()).toContainText('pulled in by prettyout')

  await page.getByRole('link', { name: 'Start chapter 01' }).click()
  await expect(page).toHaveURL(/\/workshop\/01-no-licence-no-permission$/)
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('No licence, no permission')
})

test('the explorer answers for every pair', async ({ page }) => {
  await page.goto('/#explorer')
  const explorer = page.locator('#explorer')
  const answer = explorer.getByTestId('verdict')

  await expect(answer).toHaveText('No')
  await expect(explorer.getByRole('status')).toContainText('GPL-3.0 code in an MIT project')

  await explorer.getByRole('button', { name: 'Apache-2.0', exact: true }).first().click()
  await expect(answer).toHaveText('Yes, with conditions')
  await expect(explorer.getByRole('status')).toContainText('NOTICE lines')

  await explorer.getByRole('button', { name: 'No licence' }).click()
  await expect(answer).toHaveText('No')
  await expect(explorer.getByRole('status')).toContainText('No licence means no permission')
})

test('Maggie quizzes you, and closes with Escape', async ({ page }) => {
  await page.goto('/workshop/06-names-and-logos')
  await page.getByRole('button', { name: 'Ask Maggie' }).click()
  const panel = page.getByRole('region', { name: "Maggie's notes" })
  await expect(panel).toContainText('Say what you work with')

  await panel.getByRole('button', { name: 'Official Driftwood client' }).click()
  await expect(panel.getByRole('status').first()).toContainText('Not quite.')
  await expect(panel.getByRole('button', { name: 'Driftwood-certified' })).toBeDisabled()

  await page.keyboard.press('Escape')
  await expect(panel).toBeHidden()
  await expect(page.getByRole('button', { name: 'Ask Maggie' })).toBeFocused()
})

test('every chapter renders, with its case and commands', async ({ page }) => {
  await page.goto('/workshop')
  const links = page.locator('main ol a')
  await expect(links).toHaveCount(8)
  for (const href of await links.evaluateAll((els) => els.map((el) => el.getAttribute('href')))) {
    await page.goto(href ?? '/')
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    await expect(page.locator('#commands')).toContainText('commands, from lab/')
  }
})
